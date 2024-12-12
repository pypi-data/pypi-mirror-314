from compas.datastructures import Tree

import compas_model.models  # noqa: F401
from compas_model.elements import Element  # noqa: F401

from .elementnode import ElementNode


class ElementTree(Tree):
    """Class representing the hierarchy of elements in a model through a tree.

    Parameters
    ----------
    model : :class:`compas_model.model.Model`
        The parent model of the element tree.
    name : str, optional
        The name of the tree.

    Attributes
    ----------
    model : :class:`compas_model.model.Model`
        The parent model of the tree.
    groups : list[:class:`GroupNode`], read-only
        The groups contained in the tree.
    elements : list[:class:`Element`], read-only
        The elements contained in the tree

    """

    @property
    def __data__(self):
        # type: () -> dict
        data = super(ElementTree, self).__data__
        return data

    @classmethod
    def __from_data__(cls, data):
        # type: (dict) -> ElementTree
        raise Exception("Serialisation outside model context not allowed.")

    def __init__(self, model, name=None):
        # type: (compas_model.models.Model, str | None) -> None
        super(ElementTree, self).__init__(name=name)
        self.model = model
        root = ElementNode(name="root")
        self.add(root)

    @property
    def elements(self):
        # type: () -> list[Element]
        return [node.element for node in self.nodes if isinstance(node, ElementNode) if node.element]

    def find_element_node(self, element):
        # type: (Element) -> ElementNode
        """Find the node containing the element.

        Parameters
        ----------
        element : :class:`compas_model.elements.Element`

        Returns
        -------
        :class:`compas_model.model.ElementNode`

        Raises
        ------
        ValueError
            If the element is not in the tree.

        """
        for node in self.nodes:
            if isinstance(node, ElementNode):
                if node.element is element:
                    return node
        raise ValueError("Element not in tree")
