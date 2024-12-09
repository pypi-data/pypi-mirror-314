from __future__ import annotations

from datetime import datetime

from collections.abc import Callable

from functools import update_wrapper

from typing import (
	Any, TYPE_CHECKING
)


if TYPE_CHECKING:
	from ..api import API


__H_1 = 3600


def check_login(
	func: Callable[
		..., dict[str, Any]
	]
):
	def inner(self: API, *args: ...) -> dict[str, Any]:
		self.logger.debug('Check if expired')
		c_time = datetime.now()

		if (c_time - self.token.created_at).seconds >= __H_1:
			self.refresh()

		return func(self, *args)

	update_wrapper(inner, func)

	return inner
