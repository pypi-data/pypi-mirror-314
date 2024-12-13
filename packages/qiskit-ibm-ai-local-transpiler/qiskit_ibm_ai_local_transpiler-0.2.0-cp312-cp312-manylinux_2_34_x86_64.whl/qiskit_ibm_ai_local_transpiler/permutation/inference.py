# -*- coding: utf-8 -*-

# (C) Copyright 2024 IBM. All Rights Reserved.


"""Synthesize module"""

from typing import Union
import networkx as nx
from qiskit import QuantumCircuit

from qiskit_ibm_ai_local_transpiler import qiskit_ibm_ai_local_transpiler_rs
import logging

from ..utils.transpile import (
    check_topology_synthesized_circuit,
    find_symmetries,
)

from .utils import embed_perm, get_perm_array_from_circuit, coupling_maps
from ..config.config import AITranspilerConfig

logger = logging.getLogger(__name__)
CONFIG = AITranspilerConfig()


def to_circuit(synth_out, num_qubits=None):
    if num_qubits is None:
        num_qubits = max(max(qs) for qs in synth_out) + 1
    circuit = QuantumCircuit(num_qubits)
    # circuit.barrier()
    for qs in synth_out:
        circuit.swap(*qs)
    # circuit.barrier()
    return circuit


class PermutationInference:
    RL_INFERENCE = None
    DEFAULT_N_STEPS = 10

    def __init__(
        self,
        models_info=CONFIG.ML_PERMUTATION_CONFIG.AVAILABLE_MODELS,
        models_path=CONFIG.ML_PERMUTATION_CONFIG.MODELS_PATH,
    ):
        # Auxiliary structures
        self.model_names = []
        self.model_cmap_hashes = []
        self.model_cmaps = []
        self.model_qubits = []
        self.model_topology = []
        self.model_backends = []
        models_info_rust = []
        cmaps = {}
        valid_perms = {}
        for model in models_info:
            model_name = model["model_name"]
            self.model_names.append(model_name)
            self.model_cmap_hashes.append(model["coupling_map_hash"])
            self.model_qubits.append(model["qubits"])
            self.model_topology.append(model["topology"])
            self.model_backends.append(model["backends"])
            topology = model["topology"]

            if topology is not None:
                cmap = coupling_maps.get(topology)
            else:
                cmap = coupling_maps.get(str(model["qubits"]))
            cmaps[model_name] = [tuple(item) for item in cmap]
            self.model_cmaps.append(cmap)
            # Convert all dict values to strings for rust
            model_info_rust = {
                key: str(value) if value else "" for (key, value) in model.items()
            }
            model_info_rust["coupling_map"] = str(cmap) if cmap else ""
            if cmap:
                valid_perms_list = find_symmetries(nx.Graph(cmap))
                model_info_rust["coupling_map_perms"] = str(valid_perms_list)
                valid_perms[model_name] = valid_perms_list
            else:
                model_info_rust["coupling_map_perms"] = ""
            models_info_rust.append(model_info_rust)

        # Temporary until we decouple tasks from api
        if not PermutationInference.RL_INFERENCE:
            PermutationInference.RL_INFERENCE = (
                qiskit_ibm_ai_local_transpiler_rs.PermutationSynthesis(
                    models_info_rust, cmaps, valid_perms, models_path
                )
            )

    def check_synthesized_circ(self, original_circ: list, synth_circ: QuantumCircuit):
        """Check whether a synthesized circuit does the same as another original permutation circuit"""
        synth_circ_arr = get_perm_array_from_circuit(synth_circ)

        num_q_synth = len(synth_circ_arr)
        num_q_orig = len(original_circ)
        if num_q_synth != num_q_orig:
            # We can have the situation in transpiling that the synthesized permutation needs to use
            # more qubits than the original Permutation because of the topology and its shape
            # In that case, we should embed the smaller Permutation in the max N of qubits before comparing both
            max_n_qubits = max(num_q_orig, num_q_synth)

            if num_q_orig > num_q_synth:
                synth_circ = embed_perm(perm_circ=synth_circ, nq=max_n_qubits)

            else:
                original_circ = embed_perm(perm_circ=original_circ, nq=max_n_qubits)

        return (synth_circ_arr == original_circ).all()

    def synthesize(
        self,
        perm_circ: list,
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
        circ_n_qubits = len(perm_circ)
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
            perm_circ = embed_perm(perm_circ, nq=model_n_qubits)

        if n_steps is None:
            n_steps = self.DEFAULT_N_STEPS

        logger.info(
            f"Synthesizing the permutation using the model {model_name}. "
            # f"Launching {n_steps} n_steps with n_envs {selected_model[0].info.n_envs}..."
        )

        logger.debug("Synthesizing circuit")

        # Synth the input
        try:
            gate_list = self.RL_INFERENCE.run(
                self.model_names[selected_model_id], 10, perm_circ
            )
        except Exception as err:
            raise RuntimeError(f"Inference failed: {err}")

        # gate_list = list(reversed(gate_list))

        if len(gate_list) == 0:
            return QuantumCircuit(model_n_qubits)
        rl_circuit = to_circuit(gate_list, model_n_qubits)
        logger.debug("Circuit synthesized")

        if check_result is True:
            logger.debug("Checking results from synthesis process")
            if not self.check_synthesized_circ(perm_circ, rl_circuit):
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
