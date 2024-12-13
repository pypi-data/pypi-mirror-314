from datetime import datetime
from typing import Any, Dict, Optional

import pytz
from django.db import models
from django.utils import timezone
from wbcore.contrib.io.imports import ImportExportHandler


class NewsImportHandler(ImportExportHandler):
    MODEL_APP_LABEL = "wbnews.News"

    def _deserialize(self, data: Dict[str, Any]):
        data["source"] = self.model.source_dict_to_model(data["source"])
        if parsed_datetime := data.get("datetime", None):
            data["datetime"] = pytz.utc.localize(datetime.strptime(parsed_datetime, "%Y-%m-%dT%H:%M:%S"))
        else:
            data["datetime"] = timezone.now()

    def _get_instance(self, data: Dict[str, Any], history: Optional[models.QuerySet] = None, **kwargs) -> models.Model:
        return self.model.objects.filter(source=data["source"], datetime=data["datetime"], title=data["title"]).first()

    def _create_instance(self, data: Dict[str, Any], **kwargs) -> models.Model:
        self.import_source.log += "\nCreate News."
        return self.model.objects.create(**data, import_source=self.import_source)
