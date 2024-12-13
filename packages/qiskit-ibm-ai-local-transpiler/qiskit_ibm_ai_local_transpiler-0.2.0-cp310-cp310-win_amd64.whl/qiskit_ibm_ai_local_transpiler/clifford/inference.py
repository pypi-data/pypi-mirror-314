# -*- coding: utf-8 -*-

# (C) Copyright 2024 IBM. All Rights Reserved.

"""Synthesize module"""
from typing import Union
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford
from qiskit.transpiler.passes.optimization import CXCancellation
from qiskit_ibm_ai_local_transpiler import qiskit_ibm_ai_local_transpiler_rs
import logging

from .utils import (
    embed_clifford,
    coupling_maps,
    valid_perms_topology,
    check_synthesized_clifford,
)
from ..utils.transpile import (
    check_topology_synthesized_circuit,
)

from ..config.config import AITranspilerConfig

logger = logging.getLogger(__name__)

cxc = CXCancellation()

CONFIG = AITranspilerConfig()


def cliff_to_data(cliff):
    return (
        (
            cliff.destab_x * (2**0)
            + cliff.destab_z * (2**1)
            + cliff.stab_x * (2**2)
            + cliff.stab_z * (2**3)
        )
        .flatten()
        .tolist()
    )


def solve_phases(clifford_cpy):
    num_qubits = clifford_cpy.num_qubits
    out = QuantumCircuit(num_qubits)

    # Add the phases (Pauli gates) to the Clifford circuit
    for qubit in range(num_qubits):
        stab = clifford_cpy.stab_phase[qubit]
        destab = clifford_cpy.destab_phase[qubit]
        if destab and stab:
            out.y(qubit)
        elif not destab and stab:
            out.x(qubit)
        elif destab and not stab:
            out.z(qubit)

    return out


def clean_1q_gates(qc):
    # TODO: Adapt this to new qiskit
    out = QuantumCircuit(qc.num_qubits)
    wires = [QuantumCircuit(1) for _ in range(qc.num_qubits)]
    for g in qc:
        if g.operation.name == "cx":
            q1 = g.qubits[0].index
            q2 = g.qubits[1].index
            out.compose(Clifford(wires[q1]).to_circuit(), qubits=[q1], inplace=True)
            out.compose(Clifford(wires[q2]).to_circuit(), qubits=[q2], inplace=True)
            out.cx(q1, q2)
            wires[q1] = QuantumCircuit(1)
            wires[q2] = QuantumCircuit(1)
        else:
            wires[g.qubits[0].index].compose(g.operation, qubits=[0], inplace=True)

    for qi, w in enumerate(wires):
        out.compose(Clifford(w).to_circuit(), qubits=[qi], inplace=True)

    return out


def to_circuit(synth_out, clifford_input, num_qubits=None):
    if num_qubits is None:
        num_qubits = max(max(qs) for gate, qs in synth_out) + 1
    circuit = QuantumCircuit(num_qubits)
    for gate, qs in synth_out:
        if gate == "h":
            circuit.h(qs[0])
        elif gate == "s":
            circuit.s(qs[0])
        elif gate == "cx":
            circuit.cx(*qs)
        else:
            raise RuntimeError(f"Gate {gate} not recognized")

    dcliff = Clifford(circuit).compose(clifford_input)

    out_circ = solve_phases(dcliff).compose(circuit).inverse()
    # cxc(clean_1q_gates(out_circ))

    return out_circ


def convert_perms_for_clifford_inference(perms, act_to_gate, n_qubits):
    id_perm_matrix = np.reshape(np.arange(n_qubits * n_qubits), (n_qubits, n_qubits))
    obs_perms = []
    act_perms = []
    for p in perms:
        obs_perms.append(id_perm_matrix[p, :][:, p].flatten().tolist())
        act_perm = [
            act_to_gate.index((g, tuple(p[q] for q in qs))) for g, qs in act_to_gate
        ]
        act_perms.append(act_perm)
    return obs_perms, act_perms


def build_gate_input_list(num_qbits, gate_set, coupling_map=None):
    all_gates = []
    for q_i in range(num_qbits):
        for g_i in gate_set:
            all_gates.append((g_i, (q_i,)))
        for q_j in range(q_i + 1, num_qbits):
            if coupling_map is None or [q_i, q_j] in coupling_map:
                all_gates.append(("cx", (q_i, q_j)))
            if coupling_map is None or [q_j, q_i] in coupling_map:
                all_gates.append(("cx", (q_j, q_i)))
    return all_gates


class CliffordInference:
    DEFAULT_N_STEPS = 10
    RL_INFERENCE = None

    def __init__(
        self,
        models_info=CONFIG.ML_CLIFFORD_CONFIG.AVAILABLE_MODELS,
        models_path=CONFIG.ML_CLIFFORD_CONFIG.MODELS_PATH,
    ):
        # Auxiliary structures
        self.model_names = []
        self.model_cmap_hashes = []
        self.model_cmaps = []
        self.model_qubits = []
        self.model_topology = []
        self.model_backends = []
        models_info_rust = []

        act_gates = {}
        valid_perms = {}
        valid_act_perms = {}
        for model in models_info:
            model_name = model["model_name"]
            self.model_names.append(model_name)
            self.model_cmap_hashes.append(model["coupling_map_hash"])
            self.model_qubits.append(model["qubits"])
            self.model_topology.append(model["topology"])
            self.model_backends.append(model["backends"])
            topology = model["topology"]

            # From the env
            valid_perms_list = valid_perms_topology.get(topology)
            cmap = coupling_maps.get(topology)

            act_to_gate = build_gate_input_list(model["qubits"], ["h", "s"], cmap)
            act_gates[model_name] = act_to_gate

            obs_perms, act_perms = convert_perms_for_clifford_inference(
                valid_perms_list, act_to_gate, model["qubits"]
            )

            valid_perms[model_name] = obs_perms
            valid_act_perms[model_name] = act_perms

            # TODO: Not sure if we need this
            self.model_cmaps.append(cmap)
            # Convert all dict values to strings for rust
            model_info_rust = {
                key: str(value) if value else "" for (key, value) in model.items()
            }
            models_info_rust.append(model_info_rust)

        if not CliffordInference.RL_INFERENCE:
            CliffordInference.RL_INFERENCE = (
                qiskit_ibm_ai_local_transpiler_rs.CliffordSynthesis(
                    models_info_rust,
                    act_gates,
                    valid_perms,
                    valid_act_perms,
                    models_path,
                )
            )

    def synthesize(
        self,
        cliff: Clifford,
        model_name: str = None,
        coupling_map_hash: str = None,
        backend: str = None,
        topology: str = None,
        n_qubits: int = None,
        check_result: bool = False,
        n_steps: Union[int, None] = None,
        metrics: tuple = (
            "n_cnots",
            "n_layers_cnots",
            "n_layers",
            "n_gates",
        ),
        keep_layout: bool = True,
    ) -> Union[QuantumCircuit, None]:
        """Synthesize Clifford using the RL model"""
        circ_n_qubits = cliff.num_qubits
        selected_model_id = None
        if model_name is not None and model_name in self.model_names:
            # get the model to use by its name
            selected_model_id = self.model_names.index(model_name)
        elif (
            coupling_map_hash is not None
            and coupling_map_hash in self.model_cmap_hashes
        ):
            # get the model to use depending on its coupling_map_hash
            selected_model_id = self.model_cmap_hashes.index(coupling_map_hash)
        elif backend is not None:
            # get the model to use depending the backend
            for i, backend_list in enumerate(self.model_backends):
                if backend_list and backend in backend_list:
                    selected_model_id = i
                    break

        # Topology is for now the name of the model
        elif topology is not None and topology in self.model_topology:
            # get the model to use depending the topology
            selected_model_id = self.model_topology.index(topology)
        elif n_qubits is not None and n_qubits in self.model_qubits:
            # get the model to use depending the n_qubits
            # avoid to choose models with topology for regular synthesis
            id_qubits_no_topology = [
                id
                for id, (qubits, topology) in enumerate(
                    zip(self.model_qubits, self.model_topology)
                )
                if topology is None and qubits == n_qubits
            ]
            if id_qubits_no_topology:
                selected_model_id = id_qubits_no_topology[0]
        else:
            # select the model to use depending on the N of qubits used in the permutation circuit
            # avoid to choose models with topology for regular synthesis
            # If there is no model for the current num_qubits without topology,
            # choose the next available (num_qubits +1).
            # So, if we request synthesis for 3 qubits and we only have a 3q model for I topology,
            # better use a model with more qubits but fully fully connected
            id_qubits_no_topology = [
                id
                for id, (qubits, topology) in enumerate(
                    zip(self.model_qubits, self.model_topology)
                )
                if topology is None and qubits >= circ_n_qubits
            ]
            if id_qubits_no_topology:
                selected_model_id = id_qubits_no_topology[0]

        if selected_model_id is None:
            logger.warning(
                "The model selected for inference is not available. Options used: "
                f"model_name: {model_name}, backend: {backend}, topology: {topology}, "
                f"coupling_map_hash: {coupling_map_hash}, "
                f"n_qubits: {n_qubits}, circuit n_qubits: {circ_n_qubits} "
            )
            return None
        model_name = self.model_names[selected_model_id]
        model_n_qubits = self.model_qubits[selected_model_id]
        if model_n_qubits < circ_n_qubits:
            logger.warning(
                f"The model selected for inference '{model_name}' cannot synthesize that circuit. "
                f"The model is trained for n_qubits={model_n_qubits} while the "
                f"circuits uses n_qubits={circ_n_qubits} "
            )
            return None

        # We should embed permutation also in the cases of circuits with less qubits
        # than the bakend's or topologies qubits, or the model selected manually
        if model_n_qubits > circ_n_qubits:
            cliff = embed_clifford(cliff=cliff, nq=self.model_qubits[selected_model_id])

        if n_steps is None:
            n_steps = self.DEFAULT_N_STEPS

        logger.info(
            f"Synthesizing the clifford using the model {model_name}. "
            # f"Launching {n_steps} n_steps with n_envs {selected_model[0].info.n_envs}..."
        )

        logger.debug("Synthesizing circuit")

        # Synth the input
        try:
            gate_list = self.RL_INFERENCE.run(
                self.model_names[selected_model_id], 10, cliff_to_data(cliff)
            )
        except Exception as err:
            raise RuntimeError(f"Inference failed: {err}")

        if len(gate_list) == 0:
            return QuantumCircuit(model_n_qubits)
        rl_circuit = to_circuit(gate_list, cliff, model_n_qubits)
        logger.debug("Circuit synthesized")

        if check_result is True:
            logger.debug("Checking results from synthesis process")
            if not check_synthesized_clifford(cliff, rl_circuit):
                logger.warning(
                    "The check for synthesized permutation circuit vs the original permutation failed"
                )
                return None

            if topology is not None or backend is not None:
                logger.debug(
                    "Checking if synthesized permutation follows the input topology/backend's topology"
                )
                logger.debug(
                    f"Topology: {model_name}. Coupling map: {self.model_cmaps[selected_model_id]}"
                )
                if not check_topology_synthesized_circuit(
                    rl_circuit,
                    self.model_cmaps[selected_model_id],
                ):
                    logger.warning(
                        "The check to evaluate if synthesized permutation circuit follows the topology failed"
                    )
                    return None
            logger.debug(
                "Success. The checks for the synthesis results were successful"
            )
        return rl_circuit
