from typing import Any, Callable, Final, List, Optional, Type

import pyvista
from vtkmodules.vtkCommonDataModel import vtkDataSet
from mypy.plugin import ClassDefContext, Plugin
from mypy.types import Instance

__all__: List[str] = []


def _get_type_fullname(typ: Any) -> str:
    return f"{typ.__module__}.{typ.__qualname__}"


PYVISTA_DATASET_TYPE_FULLNAME: Final = _get_type_fullname(pyvista.DataSet)
VTK_DATASET_TYPE_FULLNAME: Final = _get_type_fullname(vtkDataSet)


def _promote_dataset_callback(ctx: ClassDefContext) -> None:
    """Add two-way type promotion between `bool` and `numpy.bool_`.

    This promotion allows for use of NumPy typing annotations with `bool`,
    e.g. npt.NDArray[bool].

    See mypy.semanal_classprop.add_type_promotion for a similar promotion
    between `int` and `i64` types.
    """
    assert ctx.cls.fullname == PYVISTA_DATASET_TYPE_FULLNAME
    pyvista_dataset: Instance = ctx.api.named_type(PYVISTA_DATASET_TYPE_FULLNAME)
    vtk_dataset: Instance = ctx.api.named_type(VTK_DATASET_TYPE_FULLNAME)

    pyvista_dataset.type.alt_promote = vtk_dataset


class _PyVistaPlugin(Plugin):
    """Mypy plugin to enable type annotations of NumPy arrays with builtin types."""

    def get_customize_class_mro_hook(
        self, fullname: str
    ) -> Optional[Callable[[ClassDefContext], None]]:
        """Customize class definitions before semantic analysis."""
        if fullname == PYVISTA_DATASET_TYPE_FULLNAME:
            return _promote_dataset_callback
        return None


def plugin(version: str) -> Type[_PyVistaPlugin]:
    """Entry-point for mypy."""
    return _PyVistaPlugin
