from iemap_mi.models import FlattenedProjectBase
from typing import Optional, Dict, Any


def get_headers(token: Optional[str]) -> Dict[str, str]:
    """
    Generate headers for HTTP requests.

    Args:
        token (Optional[str]): JWT token for authentication.

    Returns:
        Dict[str, str]: Headers for HTTP requests.
    """
    headers = {}
    if token:
        headers['Authorization'] = f"Bearer {token}"
    return headers


def flatten_project_data(project: FlattenedProjectBase) -> Dict[str, Any]:
    """Flatten the project data for better compatibility with pandas DataFrame."""
    flattened = {
        'identifier': project.identifier,
        'iemap_id': project.iemap_id,
        'provenance_affiliation': project.provenance.affiliation,
        'provenance_email': project.provenance.email,
        'provenance_created_at': project.provenance.createdAt,
        'provenance_updated_at': project.provenance.updatedAt,
        'project_name': project.project.name,
        'project_label': project.project.label,
        'project_description': project.project.description,
        'process_is_experiment': project.process.isExperiment,
        'process_method': project.process.method,
        'process_agent_name': project.process.agent.name,
        'process_agent_version': project.process.agent.version,
        'material_formula': project.material.formula,
        'material_elements': ', '.join(project.material.elements),
        'parameters': ', '.join([f"{param['name']}: {param['value']}" for param in project.parameters]),
        'properties': ', '.join([f"{prop['name']}: {prop['value']}" for prop in project.properties])
    }

    # Flattening nested Input and Output structures in MaterialModel
    if project.material.input:
        flattened.update({
            'input_lattice_a': project.material.input.lattice.a,
            'input_lattice_b': project.material.input.lattice.b,
            'input_lattice_c': project.material.input.lattice.c,
            'input_lattice_alpha': project.material.input.lattice.alpha,
            'input_lattice_beta': project.material.input.lattice.beta,
            'input_lattice_gamma': project.material.input.lattice.gamma,
            'input_sites': project.material.input.sites,
            'input_species': ', '.join(project.material.input.species),
            'input_cell': project.material.input.cell
        })
    if project.material.output:
        flattened.update({
            'output_lattice_a': project.material.output.lattice.a,
            'output_lattice_b': project.material.output.lattice.b,
            'output_lattice_c': project.material.output.lattice.c,
            'output_lattice_alpha': project.material.output.lattice.alpha,
            'output_lattice_beta': project.material.output.lattice.beta,
            'output_lattice_gamma': project.material.output.lattice.gamma,
            'output_sites': project.material.output.sites,
            'output_species': ', '.join(project.material.output.species),
            'output_cell': project.material.output.cell
        })

    return flattened
