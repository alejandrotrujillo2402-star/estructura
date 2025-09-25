from .avl_node import AVLNode

class AVLTree:
    def __init__(self):
        self.root = None

    # Obtener altura de un nodo
    def _get_height(self, node):
        return node.height if node else 0

    # Calcular factor de balance
    def _get_balance(self, node):
        return self._get_height(node.left) - self._get_height(node.right) if node else 0

    # Rotaciones
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

    # Inserción (ordenado por (x,y))
    def insert(self, root, key, data=None):
        if not root:
            return AVLNode(key, data)

        if key < root.key:
            root.left = self.insert(root.left, key, data)
        elif key > root.key:
            root.right = self.insert(root.right, key, data)
        else:
            return root  # no duplicados

        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))
        balance = self._get_balance(root)

        # Casos de rotación
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
    def search_range(self, root, x_min, x_max, y_min=-9999, y_max=9999):
        """Devuelve los obstáculos dentro de un rango visible de coordenadas"""
        if not root:
            return []

        results = []
        x, y = root.key

        # Verificar si está dentro del rango
        if x_min <= x <= x_max and y_min <= y <= y_max:
            results.append(root.data)

        # Buscar en subárbol izquierdo
        if root.left and x >= x_min:
            results.extend(self.search_range(root.left, x_min, x_max, y_min, y_max))

        # Buscar en subárbol derecho
        if root.right and x <= x_max:
            results.extend(self.search_range(root.right, x_min, x_max, y_min, y_max))

        return results

