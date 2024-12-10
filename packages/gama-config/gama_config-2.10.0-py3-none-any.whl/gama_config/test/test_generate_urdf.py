from gama_config.generate_urdf import generate_urdf
from gama_config.gama_vessel import ArmidaleVesselConfig
from greenstream_config import Offsets


def test_generate_urdf():
    urdf = generate_urdf(
        config=ArmidaleVesselConfig(),
        ins_offset=Offsets(),
        mesh_path="package://some_package/meshes/some_mesh.stl",
    )

    assert """<mesh filename="package://some_package/meshes/some_mesh.stl"/>""" in urdf
