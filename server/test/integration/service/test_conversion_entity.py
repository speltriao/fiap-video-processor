import os

import pytest
from mockito import any as ANY
from mockito import unstub, when

from server.domain.service.conversion_service import ConversionService
from server.test import return_none
from server.test.integration import ABCTestBase


class TestConversionService(ABCTestBase):
    @pytest.mark.asyncio
    async def test_conversion_success(self):
        conversion_service = ConversionService()
        conversion = self._mock_conversion
        when(os).makedirs(ANY(), exist_ok=True).thenReturn(None)
        when(conversion_service)._convert_video(ANY(), ANY()).thenReturn(return_none())
        result = await conversion_service.create_conversion(conversion)
        assert result.id == 1
        unstub()
