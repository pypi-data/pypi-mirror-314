__all__ = [
    'AsyncExpertsPortalBonusesClient',
    'PerformerBonusForm',
]

from toloka.a9s.client.base.client import AsyncBaseExpertsPortalClient
from toloka.a9s.client.models.generated.ai.toloka.experts.portal.money.web.performer_bonus.form import (
    PerformerBonusForm,
)
from toloka.a9s.client.models.utils import model_dump_a9s


class AsyncExpertsPortalBonusesClient(AsyncBaseExpertsPortalClient):
    async def upload_performer_bonus(self, form: PerformerBonusForm) -> None:
        await self.client.make_request(
            method='POST',
            url=f'{self.V1_PREFIX}/performer-bonuses/upload',
            body=model_dump_a9s(form),
        )
