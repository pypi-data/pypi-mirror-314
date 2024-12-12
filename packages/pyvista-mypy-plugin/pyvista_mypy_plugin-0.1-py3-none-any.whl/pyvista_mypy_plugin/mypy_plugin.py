from typing import Any, Callable, Final, List, Optional, Type

from pyvista.core.dataset import DataSet, DataObject
from pyvista.core.pointset import _PointSet
from vtkmodules.vtkCommonDataModel import vtkDataSet, vtkDataObject, vtkPointSet
from mypy.plugin import ClassDefContext, Plugin
from mypy.types import Instance

__all__: List[str] = []


def _get_type_fullname(typ: Any) -> str:
    return f"{typ.__module__}.{typ.__qualname__}"


PYVISTA_POINTSET_TYPE_FULLNAME: Final = _get_type_fullname(_PointSet)
VTK_POINTSET_TYPE_FULLNAME: Final = _get_type_fullname(vtkPointSet)

PYVISTA_DATASET_TYPE_FULLNAME: Final = _get_type_fullname(DataSet)
VTK_DATASET_TYPE_FULLNAME: Final = _get_type_fullname(vtkDataSet)

PYVISTA_DATAOBJECT_TYPE_FULLNAME: Final = _get_type_fullname(DataObject)
VTK_DATAOBJECT_TYPE_FULLNAME: Final = _get_type_fullname(vtkDataObject)


def _promote_pointset_callback(ctx: ClassDefContext) -> None:
    """Add one-way type promotion so that a pyvista _PointSet is a vtkPointSet."""
    assert ctx.cls.fullname == PYVISTA_POINTSET_TYPE_FULLNAME
    pyvista_type: Instance = ctx.api.named_type(PYVISTA_POINTSET_TYPE_FULLNAME)
    vtk_type: Instance = ctx.api.named_type(VTK_POINTSET_TYPE_FULLNAME)

    pyvista_type.type._promote.append(vtk_type)


def _promote_dataset_callback(ctx: ClassDefContext) -> None:
    """Add one-way type promotion so that a pyvista DataSet is a vtkDataSet."""
    assert ctx.cls.fullname == PYVISTA_DATASET_TYPE_FULLNAME
    pyvista_type: Instance = ctx.api.named_type(PYVISTA_DATASET_TYPE_FULLNAME)
    vtk_type: Instance = ctx.api.named_type(VTK_DATASET_TYPE_FULLNAME)

    pyvista_type.type._promote.append(vtk_type)


def _promote_dataobject_callback(ctx: ClassDefContext) -> None:
    """Add one-way type promotion so that a pyvista DataObject is a vtkDataObject."""
    assert ctx.cls.fullname == PYVISTA_DATAOBJECT_TYPE_FULLNAME
    pyvista_type: Instance = ctx.api.named_type(PYVISTA_DATAOBJECT_TYPE_FULLNAME)
    vtk_type: Instance = ctx.api.named_type(VTK_DATAOBJECT_TYPE_FULLNAME)

    pyvista_type.type._promote.append(vtk_type)


class _PyVistaPlugin(Plugin):
    """Mypy plugin to enable type promotions with VTK types."""

    def get_customize_class_mro_hook(
        self, fullname: str
    ) -> Optional[Callable[[ClassDefContext], None]]:
        """Customize class definitions before semantic analysis."""
        if fullname == PYVISTA_POINTSET_TYPE_FULLNAME:
            return _promote_pointset_callback
        elif fullname == PYVISTA_DATASET_TYPE_FULLNAME:
            return _promote_dataset_callback
        elif fullname == PYVISTA_DATAOBJECT_TYPE_FULLNAME:
            return _promote_dataobject_callback
        return None


def plugin(version: str) -> Type[_PyVistaPlugin]:
    """Entry-point for mypy."""
    return _PyVistaPlugin
