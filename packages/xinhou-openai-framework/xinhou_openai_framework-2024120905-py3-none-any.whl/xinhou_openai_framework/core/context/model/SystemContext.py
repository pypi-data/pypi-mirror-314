# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
全局系统上下文的存储及初始化模型存储
----------------------------------------------------
@Project :   xinhou-openai-framework
@File    :   SystemContext.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/1/19 18:07   shenpeng   1.0         None
"""

from contextvars import ContextVar, Token
from typing import Any, Dict

from starlette.types import ASGIApp, Receive, Scope, Send


class SystemContext:
    __slots__ = ("_vars", "_reset_tokens")

    _vars: Dict[str, ContextVar]
    _reset_tokens: Dict[str, Token]

    def __init__(self) -> None:
        object.__setattr__(self, "_vars", {})
        object.__setattr__(self, "_reset_tokens", {})

    def reset(self) -> None:
        for _name, var in self._vars.items():
            try:
                var.reset(self._reset_tokens[_name])
            except ValueError:
                var.set(None)

    def _ensure_var(self, item: str) -> None:
        if item not in self._vars:
            self._vars[item] = ContextVar(f"globals:{item}", default=None)
            self._reset_tokens[item] = self._vars[item].set(None)

    def __getattr__(self, item: str) -> Any:
        return self._vars[item].get()

    def __setattr__(self, item: str, value: Any) -> None:
        self._ensure_var(item)
        self._vars[item].set(value)


class GlobalsMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "lifespan":
            ctx.reset()
        await self.app(scope, receive, send)


ctx = SystemContext()
