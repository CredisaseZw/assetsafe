from django.test import SimpleTestCase

from apps.enquiries.services.masking import (
    mask_company_name,
    mask_id_reg_display,
    mask_identification,
    mask_individual_name,
)


class MaskingTests(SimpleTestCase):
    def test_mask_individual_name(self):
        self.assertEqual(mask_individual_name("George", "Abba"), "Ge.... .....ba")

    def test_mask_company_name_single_word(self):
        self.assertTrue(mask_company_name("ReiCorp").startswith("Rei"))

    def test_mask_company_name_multi_word(self):
        masked = mask_company_name("Reimambo (Pvt) Ltd")
        self.assertTrue(masked.startswith("Rei"))
        self.assertTrue(masked.endswith("td"))

    def test_mask_identification(self):
        self.assertEqual(mask_identification("XX0R63"), ".....0R63")
        self.assertEqual(
            mask_identification("189999", is_registration_number=True), "189...."
        )

    def test_mask_id_reg_display(self):
        result = mask_id_reg_display("xx0R63", "1899")
        self.assertIn("/", result)
