from ..models.duplicated_document_models import DuplicatedDocument
from ..permissions import permission_document_tools, permission_document_view

from .base import GenericDocumentViewTestCase
from .mixins import (
    DuplicatedDocumentToolViewTestMixin, DuplicatedDocumentsViewsTestMixin
)


class DocumentsDuplicatesViewsTestCase(
    DuplicatedDocumentsViewsTestMixin, GenericDocumentViewTestCase
):
    def test_document_duplicates_list_no_permission(self):
        self._upload_duplicate_document()

        response = self._request_document_duplicates_list_view()
        self.assertEqual(response.status_code, 404)

    def test_document_duplicates_list_with_source_access(self):
        self._upload_duplicate_document()
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_document_view
        )

        response = self._request_document_duplicates_list_view()
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_documents[1].label
        )

    def test_document_duplicates_list_with_target_access(self):
        self._upload_duplicate_document()

        self.grant_access(
            obj=self.test_documents[1],
            permission=permission_document_view
        )

        response = self._request_document_duplicates_list_view()
        self.assertEqual(response.status_code, 404)

    def test_document_duplicates_list_with_full_access(self):
        self._upload_duplicate_document()
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_documents[1],
            permission=permission_document_view
        )

        response = self._request_document_duplicates_list_view()
        self.assertContains(
            response=response, status_code=200,
            text=self.test_documents[1].label
        )

    def test_document_duplicates_list_trashed_source_with_full_access(self):
        self._upload_duplicate_document()
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_documents[1],
            permission=permission_document_view
        )

        self.test_documents[0].delete()

        response = self._request_document_duplicates_list_view()
        self.assertEqual(response.status_code, 404)

    def test_document_duplicates_list_trashed_target_with_full_access(self):
        self._upload_duplicate_document()
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_documents[1],
            permission=permission_document_view
        )

        self.test_documents[1].delete()

        response = self._request_document_duplicates_list_view()
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_documents[1].label
        )


class DuplicatedDocumentsViewsTestCase(
    DuplicatedDocumentsViewsTestMixin, GenericDocumentViewTestCase
):
    def test_duplicated_document_list_no_permission(self):
        self._upload_duplicate_document()

        response = self._request_duplicated_document_list_view()
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_documents[0].label
        )

    def test_duplicated_document_list_with_source_access(self):
        self._upload_duplicate_document()
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_document_view
        )

        response = self._request_duplicated_document_list_view()
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_documents[0].label
        )
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_documents[1].label
        )

    def test_duplicated_document_list_with_target_access(self):
        self._upload_duplicate_document()

        self.grant_access(
            obj=self.test_documents[1],
            permission=permission_document_view
        )

        response = self._request_duplicated_document_list_view()
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_documents[0].label
        )
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_documents[1].label
        )

    def test_duplicated_document_list_with_full_access(self):
        self._upload_duplicate_document()
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_documents[1],
            permission=permission_document_view
        )

        response = self._request_duplicated_document_list_view()
        self.assertContains(
            response=response, status_code=200,
            text=self.test_documents[0].label
        )
        self.assertContains(
            response=response, status_code=200,
            text=self.test_documents[1].label
        )

    def test_duplicated_document_list_trashed_source_with_full_access(self):
        self._upload_duplicate_document()
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_documents[1],
            permission=permission_document_view
        )

        self.test_documents[0].delete()

        response = self._request_duplicated_document_list_view()
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_documents[0].label
        )
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_documents[1].label
        )

    def test_duplicated_document_list_trashed_target_with_full_access(self):
        self._upload_duplicate_document()
        self.grant_access(
            obj=self.test_documents[0],
            permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_documents[1],
            permission=permission_document_view
        )

        self.test_documents[1].delete()

        response = self._request_duplicated_document_list_view()
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_documents[0].label
        )
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_documents[1].label
        )


class DuplicatedDocumentToolsViewsTestCase(
    DuplicatedDocumentToolViewTestMixin, DuplicatedDocumentsViewsTestMixin,
    GenericDocumentViewTestCase
):
    def test_duplicated_document_scan_no_permission(self):
        self._upload_duplicate_document()
        DuplicatedDocument.objects.all().delete()

        response = self._request_duplicated_document_scan_view()
        self.assertEqual(response.status_code, 403)

        self.assertFalse(
            self.test_documents[1] in DuplicatedDocument.objects.get_duplicates_of(
                document=self.test_documents[0]
            )
        )

    def test_duplicated_document_scan_with_permission(self):
        self._upload_duplicate_document()
        DuplicatedDocument.objects.all().delete()

        self.grant_permission(permission=permission_document_tools)

        response = self._request_duplicated_document_scan_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self.test_documents[1] in DuplicatedDocument.objects.get_duplicates_of(
                document=self.test_documents[0]
            )
        )
