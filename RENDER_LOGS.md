

May 8, 2:16 AM - 2:21 AM
GMT+5:30
---
2026-05-07T20:50:40.229793746Z   File "/opt/render/project/python/Python-3.11.9/lib/python3.11/asyncio/runners.py", line 118, in run
2026-05-07T20:50:40.229886612Z     return self._loop.run_until_complete(task)
2026-05-07T20:50:40.229894463Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-07T20:50:40.229898333Z   File "uvloop/loop.pyx", line 1518, in uvloop.loop.Loop.run_until_complete
2026-05-07T20:50:40.230040753Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/uvicorn/server.py", line 69, in serve
2026-05-07T20:50:40.230132189Z     await self._serve(sockets)
2026-05-07T20:50:40.23014282Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/uvicorn/server.py", line 76, in _serve
2026-05-07T20:50:40.230227286Z     config.load()
2026-05-07T20:50:40.230232226Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/uvicorn/config.py", line 433, in load
2026-05-07T20:50:40.230387427Z     self.loaded_app = import_from_string(self.app)
2026-05-07T20:50:40.230394347Z                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-07T20:50:40.230397858Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/uvicorn/importer.py", line 22, in import_from_string
2026-05-07T20:50:40.230493825Z     raise exc from None
2026-05-07T20:50:40.230500095Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/uvicorn/importer.py", line 19, in import_from_string
2026-05-07T20:50:40.23056929Z     module = importlib.import_module(module_str)
2026-05-07T20:50:40.23057371Z              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-07T20:50:40.23057754Z   File "/opt/render/project/python/Python-3.11.9/lib/python3.11/importlib/__init__.py", line 126, in import_module
2026-05-07T20:50:40.230676017Z     return _bootstrap._gcd_import(name[level:], package, level)
2026-05-07T20:50:40.230711689Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-07T20:50:40.23071507Z   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2026-05-07T20:50:40.23071778Z   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2026-05-07T20:50:40.23072038Z   File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2026-05-07T20:50:40.23072335Z   File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2026-05-07T20:50:40.23072595Z   File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2026-05-07T20:50:40.230728551Z   File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2026-05-07T20:50:40.230734401Z   File "/opt/render/project/src/backend/main.py", line 7, in <module>
2026-05-07T20:50:40.230794135Z     from db.session import init_db
2026-05-07T20:50:40.230796926Z   File "/opt/render/project/src/backend/db/session.py", line 44, in <module>
2026-05-07T20:50:40.230909763Z     engine = _build_engine()
2026-05-07T20:50:40.230915284Z              ^^^^^^^^^^^^^^^
2026-05-07T20:50:40.230919004Z   File "/opt/render/project/src/backend/db/session.py", line 32, in _build_engine
2026-05-07T20:50:40.23100518Z     return create_async_engine(
2026-05-07T20:50:40.2310086Z            ^^^^^^^^^^^^^^^^^^^^
2026-05-07T20:50:40.23101228Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/sqlalchemy/ext/asyncio/engine.py", line 120, in create_async_engine
2026-05-07T20:50:40.231129338Z     sync_engine = _create_engine(url, **kw)
2026-05-07T20:50:40.23114826Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-07T20:50:40.2311539Z   File "<string>", line 2, in create_engine
2026-05-07T20:50:40.231157771Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/sqlalchemy/util/deprecations.py", line 281, in warned
2026-05-07T20:50:40.231286849Z     return fn(*args, **kwargs)  # type: ignore[no-any-return]
2026-05-07T20:50:40.23129409Z            ^^^^^^^^^^^^^^^^^^^
2026-05-07T20:50:40.2312971Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 599, in create_engine
2026-05-07T20:50:40.231491963Z     dbapi = dbapi_meth(**dbapi_args)
2026-05-07T20:50:40.231497614Z             ^^^^^^^^^^^^^^^^^^^^^^^^
2026-05-07T20:50:40.231501594Z   File "/opt/render/project/src/.venv/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/psycopg2.py", line 690, in import_dbapi
2026-05-07T20:50:40.231884671Z     import psycopg2
2026-05-07T20:50:40.231890151Z ModuleNotFoundError: No module named 'psycopg2'
2026-05-07T20:50:41.793379441Z ==> No open ports detected, continuing to scan...
2026-05-07T20:50:42.222597596Z ==> Docs on specifying a port: https://render.com/docs/web-services#port-binding
2026-05-07T20:50:44.070434196Z ==> Exited with status 1
2026-05-07T20:50:44.073198931Z ==> Common ways to troubleshoot your deploy: https://render.com/docs/troubleshooting-deploys
---