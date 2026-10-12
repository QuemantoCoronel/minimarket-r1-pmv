import unittest
from decimal import Decimal, InvalidOperation


class ProductoEnlatadoContractValidator:
    """
    Arnés de auditoría técnica para S1-PROD02-REV (HU-PROD-02).
    Verifica que las reglas críticas (RN / CA / NFR) se cumplan estrictamente:
    1. Exclusividad de rol ADMIN (AUTHZ en servidor).
    2. Prohibición absoluta de float para dinero (solo Decimal exacto con 2 decimales).
    3. Precio de venta estrictamente > Decimal('0.00').
    4. Unicidad de código/SKU de producto enlatado y campos obligatorios.
    """

    def __init__(self):
        self._catalogo_skus = set()

    def registrar_producto(self, *, actor_role: str, sku: str, nombre: str, precio_venta):
        # CA / NFR Seguridad: Autorización real en servidor exclusiva para ADMIN
        if actor_role != "ADMIN":
            return {"ok": False, "status": 403, "error": "Acceso denegado: se requiere rol ADMIN"}

        # Validación de campos obligatorios
        sku_clean = (sku or "").strip().upper()
        nombre_clean = (nombre or "").strip()
        if not sku_clean or not nombre_clean:
            return {"ok": False, "status": 400, "error": "SKU y nombre son obligatorios"}

        # Prohibición estricta de float para dinero
        if isinstance(precio_venta, float):
            raise TypeError("Prohibido usar float para montos monetarios; use Decimal exacto.")

        try:
            if not isinstance(precio_venta, Decimal):
                precio_dec = Decimal(str(precio_venta))
            else:
                precio_dec = precio_venta
        except (InvalidOperation, ValueError):
            return {"ok": False, "status": 400, "error": "Formato de precio inválido"}

        # RN / CA: Precio debe ser mayor que 0.00 y tener precisión de 2 decimales
        if precio_dec <= Decimal("0.00"):
            return {"ok": False, "status": 400, "error": "El precio de venta debe ser mayor a 0.00"}

        if precio_dec.as_tuple().exponent < -2:
            return {"ok": False, "status": 400, "error": "El precio no puede exceder 2 decimales"}

        # RN / CA: Unicidad de SKU
        if sku_clean in self._catalogo_skus:
            return {"ok": False, "status": 409, "error": "El código SKU ya se encuentra registrado"}

        self._catalogo_skus.add(sku_clean)
        return {
            "ok": True,
            "status": 201,
            "producto": {
                "sku": sku_clean,
                "nombre": nombre_clean,
                "precio_venta": precio_dec.quantize(Decimal("0.01")),
            },
        }


class TestS1Prod02RevAudit(unittest.TestCase):
    def setUp(self):
        self.validator = ProductoEnlatadoContractValidator()

    def test_01_admin_puede_registrar_producto_con_decimal_exacto(self):
        res = self.validator.registrar_producto(
            actor_role="ADMIN",
            sku="ENL-ATUN-001",
            nombre="Atún Filete en Aceite 170g",
            precio_venta=Decimal("6.50"),
        )
        self.assertTrue(res["ok"])
        self.assertEqual(res["status"], 201)
        self.assertIsInstance(res["producto"]["precio_venta"], Decimal)
        self.assertEqual(res["producto"]["precio_venta"], Decimal("6.50"))

    def test_02_bloqueo_403_para_almacenero_y_vendedor(self):
        for rol_no_autorizado in ("ALMACENERO", "VENDEDOR"):
            res = self.validator.registrar_producto(
                actor_role=rol_no_autorizado,
                sku="ENL-DURAZNO-002",
                nombre="Duraznos en Almíbar 820g",
                precio_venta=Decimal("11.90"),
            )
            self.assertFalse(res["ok"])
            self.assertEqual(res["status"], 403)

    def test_03_prohibicion_estricta_de_float_en_precio(self):
        with self.assertRaises(TypeError):
            self.validator.registrar_producto(
                actor_role="ADMIN",
                sku="ENL-LECHE-003",
                nombre="Leche Evaporada Entera 400g",
                precio_venta=4.50,  # float prohibido por regla del proyecto
            )

    def test_04_rechazo_precio_cero_o_negativo(self):
        for monto_invalido in (Decimal("0.00"), Decimal("-3.20")):
            res = self.validator.registrar_producto(
                actor_role="ADMIN",
                sku="ENL-MAIZ-004",
                nombre="Maíz Dulce Enlatado 300g",
                precio_venta=monto_invalido,
            )
            self.assertFalse(res["ok"])
            self.assertEqual(res["status"], 400)

    def test_05_rechazo_sku_duplicado(self):
        primero = self.validator.registrar_producto(
            actor_role="ADMIN",
            sku="ENL-SARDINA-005",
            nombre="Sardinas en Salsa de Tomate 425g",
            precio_venta=Decimal("5.80"),
        )
        self.assertTrue(primero["ok"])

        duplicado = self.validator.registrar_producto(
            actor_role="ADMIN",
            sku="enl-sardina-005",
            nombre="Sardinas Duplicadas",
            precio_venta=Decimal("6.00"),
        )
        self.assertFalse(duplicado["ok"])
        self.assertEqual(duplicado["status"], 409)


if __name__ == "__main__":
    unittest.main(verbosity=2)