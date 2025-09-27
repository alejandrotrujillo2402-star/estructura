# avl/avl_tree.py
from .avl_node import AVLNode

class AVLTree:
    def __init__(self):
        self.root = None

    # --- utilidades ---
    def _get_height(self, node):
        return node.height if node else 0

    def _get_balance(self, node):
        return self._get_height(node.left) - self._get_height(node.right) if node else 0

    def _right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))
        return x

    def _left_rotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    # --- inserción pública (wrapper) ---
    def insert(self, root, key, data=None):
        if not root:
            return AVLNode(key, data)

        if key < root.key:
            root.left = self.insert(root.left, key, data)
        elif key > root.key:
            root.right = self.insert(root.right, key, data)
        else:
            # no permitimos claves repetidas
            return root

        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))
        balance = self._get_balance(root)

        # Rotaciones según caso
        if balance > 1 and key < root.left.key:
            return self._right_rotate(root)
        if balance < -1 and key > root.right.key:
            return self._left_rotate(root)
        if balance > 1 and key > root.left.key:
            root.left = self._left_rotate(root.left)
            return self._right_rotate(root)
        if balance < -1 and key < root.right.key:
            root.right = self._right_rotate(root.right)
            return self._left_rotate(root)

        return root

    # --- buscar mínimo (sucesor) ---
    def get_min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    # --- eliminación segura ---
    def delete(self, root, key):
        if not root:
            return root

        # localizar
        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            # encontrado
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            else:
                # dos hijos: reemplazar con sucesor
                temp = self.get_min_value_node(root.right)
                # copiar clave y data del sucesor
                root.key = temp.key
                root.data = temp.data
                root.right = self.delete(root.right, temp.key)

        # si se devolvió None (subárbol vacío)
        if not root:
            return root

        # actualizar altura y balancear
        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))
        balance = self._get_balance(root)

        # rotaciones
        if balance > 1 and self._get_balance(root.left) >= 0:
            return self._right_rotate(root)
        if balance > 1 and self._get_balance(root.left) < 0:
            root.left = self._left_rotate(root.left)
            return self._right_rotate(root)
        if balance < -1 and self._get_balance(root.right) <= 0:
            return self._left_rotate(root)
        if balance < -1 and self._get_balance(root.right) > 0:
            root.right = self._right_rotate(root.right)
            return self._left_rotate(root)

        return root

    # --- recorrido en rango (x_min, x_max) ---
    def search_range(self, root, x_min, x_max, y_min=-9999, y_max=9999):
        if not root:
            return []

        results = []
        x, y = root.key

        # si la clave está dentro del rango
        if x_min <= x <= x_max and y_min <= y <= y_max:
            results.append(root.data)

        # recortar búsqueda por x
        if root.left and x >= x_min:
            results.extend(self.search_range(root.left, x_min, x_max, y_min, y_max))
        if root.right and x <= x_max:
            results.extend(self.search_range(root.right, x_min, x_max, y_min, y_max))

        return results

    # --- inorder (debug) ---
    def inorder(self, root):
        if not root:
            return []
        return self.inorder(root.left) + [(root.key, getattr(root, "data", None))] + self.inorder(root.right)
