

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


  Using cached watchfiles-1.1.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (4.9 kB)
Collecting websockets>=10.4 (from uvicorn[standard]==0.29.0->-r requirements.txt (line 2))
  Using cached websockets-16.0-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl.metadata (6.8 kB)
Collecting dnspython>=2.0.0 (from email_validator>=2.0.0->fastapi==0.111.0->-r requirements.txt (line 1))
  Using cached dnspython-2.8.0-py3-none-any.whl.metadata (5.7 kB)
Collecting typer>=0.16.0 (from fastapi-cli>=0.0.2->fastapi==0.111.0->-r requirements.txt (line 1))
  Using cached typer-0.25.1-py3-none-any.whl.metadata (15 kB)
Collecting rich-toolkit>=0.14.8 (from fastapi-cli>=0.0.2->fastapi==0.111.0->-r requirements.txt (line 1))
  Using cached rich_toolkit-0.19.7-py3-none-any.whl.metadata (1.0 kB)
Collecting googleapis-common-protos<2.0.0,>=1.63.2 (from google-api-core!=2.0.*,!=2.1.*,!=2.2.*,!=2.3.0,<3.0.0.dev0,>=1.31.5->google-api-python-client==2.129.0->-r requirements.txt (line 18))
  Using cached googleapis_common_protos-1.75.0-py3-none-any.whl.metadata (8.6 kB)
Collecting protobuf<8.0.0,>=4.25.8 (from google-api-core!=2.0.*,!=2.1.*,!=2.2.*,!=2.3.0,<3.0.0.dev0,>=1.31.5->google-api-python-client==2.129.0->-r requirements.txt (line 18))
  Using cached protobuf-7.34.1-cp310-abi3-manylinux2014_x86_64.whl.metadata (595 bytes)
Collecting proto-plus<2.0.0,>=1.22.3 (from google-api-core!=2.0.*,!=2.1.*,!=2.2.*,!=2.3.0,<3.0.0.dev0,>=1.31.5->google-api-python-client==2.129.0->-r requirements.txt (line 18))
  Using cached proto_plus-1.28.0-py3-none-any.whl.metadata (2.2 kB)
Collecting requests<3.0.0,>=2.20.0 (from google-api-core!=2.0.*,!=2.1.*,!=2.2.*,!=2.3.0,<3.0.0.dev0,>=1.31.5->google-api-python-client==2.129.0->-r requirements.txt (line 18))
  Using cached requests-2.33.1-py3-none-any.whl.metadata (4.8 kB)
Collecting pyparsing<4,>=3.1 (from httplib2<1.dev0,>=0.19.0->google-api-python-client==2.129.0->-r requirements.txt (line 18))
  Using cached pyparsing-3.3.2-py3-none-any.whl.metadata (5.8 kB)
Collecting MarkupSafe>=2.0 (from jinja2>=2.11.2->fastapi==0.111.0->-r requirements.txt (line 1))
  Using cached markupsafe-3.0.3-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (2.7 kB)
Collecting pyasn1<0.7.0,>=0.6.1 (from pyasn1-modules>=0.2.1->google-auth==2.29.0->-r requirements.txt (line 16))
  Using cached pyasn1-0.6.3-py3-none-any.whl.metadata (8.4 kB)
Collecting oauthlib>=3.0.0 (from requests-oauthlib>=0.7.0->google-auth-oauthlib==1.2.0->-r requirements.txt (line 17))
  Using cached oauthlib-3.3.1-py3-none-any.whl.metadata (7.9 kB)
Collecting huggingface-hub<2.0,>=0.16.4 (from tokenizers>=0.13.0->anthropic==0.26.1->-r requirements.txt (line 22))
  Using cached huggingface_hub-1.14.0-py3-none-any.whl.metadata (14 kB)
Collecting filelock>=3.10.0 (from huggingface-hub<2.0,>=0.16.4->tokenizers>=0.13.0->anthropic==0.26.1->-r requirements.txt (line 22))
  Using cached filelock-3.29.0-py3-none-any.whl.metadata (2.0 kB)
Collecting fsspec>=2023.5.0 (from huggingface-hub<2.0,>=0.16.4->tokenizers>=0.13.0->anthropic==0.26.1->-r requirements.txt (line 22))
  Using cached fsspec-2026.4.0-py3-none-any.whl.metadata (10 kB)
Collecting hf-xet<2.0.0,>=1.4.3 (from huggingface-hub<2.0,>=0.16.4->tokenizers>=0.13.0->anthropic==0.26.1->-r requirements.txt (line 22))
  Using cached hf_xet-1.5.0-cp37-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (4.9 kB)
Collecting packaging>=20.9 (from huggingface-hub<2.0,>=0.16.4->tokenizers>=0.13.0->anthropic==0.26.1->-r requirements.txt (line 22))
  Using cached packaging-26.2-py3-none-any.whl.metadata (3.5 kB)
Collecting tqdm>=4.42.1 (from huggingface-hub<2.0,>=0.16.4->tokenizers>=0.13.0->anthropic==0.26.1->-r requirements.txt (line 22))
  Using cached tqdm-4.67.3-py3-none-any.whl.metadata (57 kB)
Collecting charset_normalizer<4,>=2 (from requests<3.0.0,>=2.20.0->google-api-core!=2.0.*,!=2.1.*,!=2.2.*,!=2.3.0,<3.0.0.dev0,>=1.31.5->google-api-python-client==2.129.0->-r requirements.txt (line 18))
  Using cached charset_normalizer-3.4.7-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (40 kB)
Collecting urllib3<3,>=1.26 (from requests<3.0.0,>=2.20.0->google-api-core!=2.0.*,!=2.1.*,!=2.2.*,!=2.3.0,<3.0.0.dev0,>=1.31.5->google-api-python-client==2.129.0->-r requirements.txt (line 18))
  Using cached urllib3-2.7.0-py3-none-any.whl.metadata (6.9 kB)
Collecting rich>=13.7.1 (from rich-toolkit>=0.14.8->fastapi-cli>=0.0.2->fastapi==0.111.0->-r requirements.txt (line 1))
  Using cached rich-15.0.0-py3-none-any.whl.metadata (18 kB)
Collecting shellingham>=1.3.0 (from typer>=0.16.0->fastapi-cli>=0.0.2->fastapi==0.111.0->-r requirements.txt (line 1))
  Using cached shellingham-1.5.4-py2.py3-none-any.whl.metadata (3.5 kB)
Collecting annotated-doc>=0.0.2 (from typer>=0.16.0->fastapi-cli>=0.0.2->fastapi==0.111.0->-r requirements.txt (line 1))
  Using cached annotated_doc-0.0.4-py3-none-any.whl.metadata (6.6 kB)
Collecting markdown-it-py>=2.2.0 (from rich>=13.7.1->rich-toolkit>=0.14.8->fastapi-cli>=0.0.2->fastapi==0.111.0->-r requirements.txt (line 1))
  Using cached markdown_it_py-4.2.0-py3-none-any.whl.metadata (7.4 kB)
Collecting pygments<3.0.0,>=2.13.0 (from rich>=13.7.1->rich-toolkit>=0.14.8->fastapi-cli>=0.0.2->fastapi==0.111.0->-r requirements.txt (line 1))
  Using cached pygments-2.20.0-py3-none-any.whl.metadata (2.5 kB)
Collecting mdurl~=0.1 (from markdown-it-py>=2.2.0->rich>=13.7.1->rich-toolkit>=0.14.8->fastapi-cli>=0.0.2->fastapi==0.111.0->-r requirements.txt (line 1))
  Using cached mdurl-0.1.2-py3-none-any.whl.metadata (1.6 kB)
Using cached fastapi-0.111.0-py3-none-any.whl (91 kB)
Using cached uvicorn-0.29.0-py3-none-any.whl (60 kB)
Using cached pydantic-2.7.1-py3-none-any.whl (409 kB)
Using cached pydantic_settings-2.2.1-py3-none-any.whl (13 kB)
Using cached SQLAlchemy-2.0.30-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.2 MB)
Using cached asyncpg-0.29.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.8 MB)
Using cached alembic-1.13.1-py3-none-any.whl (233 kB)
Using cached httpx-0.27.0-py3-none-any.whl (75 kB)
Using cached python_dotenv-1.0.1-py3-none-any.whl (19 kB)
Using cached APScheduler-3.10.4-py3-none-any.whl (59 kB)
Using cached python_telegram_bot-21.3-py3-none-any.whl (631 kB)
Using cached feedparser-6.0.11-py3-none-any.whl (81 kB)
Using cached beautifulsoup4-4.12.3-py3-none-any.whl (147 kB)
Using cached lxml-5.2.2-cp311-cp311-manylinux_2_28_x86_64.whl (5.0 MB)
Using cached notion_client-2.2.1-py2.py3-none-any.whl (13 kB)
Using cached google_auth-2.29.0-py2.py3-none-any.whl (189 kB)
Using cached google_auth_oauthlib-1.2.0-py2.py3-none-any.whl (24 kB)
Using cached google_api_python_client-2.129.0-py2.py3-none-any.whl (11.6 MB)
Using cached python_multipart-0.0.9-py3-none-any.whl (22 kB)
Using cached aiofiles-23.2.1-py3-none-any.whl (15 kB)
Using cached tenacity-8.3.0-py3-none-any.whl (25 kB)
Using cached anthropic-0.26.1-py3-none-any.whl (877 kB)
Using cached httpcore-1.0.9-py3-none-any.whl (78 kB)
Using cached pydantic_core-2.18.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.1 MB)
Using cached annotated_types-0.7.0-py3-none-any.whl (13 kB)
Using cached anyio-4.13.0-py3-none-any.whl (114 kB)
Using cached async_timeout-5.0.1-py3-none-any.whl (6.2 kB)
Using cached cachetools-5.5.2-py3-none-any.whl (10 kB)
Using cached click-8.3.3-py3-none-any.whl (110 kB)
Using cached distro-1.9.0-py3-none-any.whl (20 kB)
Using cached email_validator-2.3.0-py3-none-any.whl (35 kB)
Using cached fastapi_cli-0.0.24-py3-none-any.whl (12 kB)
Using cached google_api_core-2.30.3-py3-none-any.whl (173 kB)
Using cached google_auth_httplib2-0.4.0-py3-none-any.whl (9.5 kB)
Using cached greenlet-3.5.0-cp311-cp311-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (615 kB)
Using cached h11-0.16.0-py3-none-any.whl (37 kB)
Using cached httplib2-0.31.2-py3-none-any.whl (91 kB)
Using cached httptools-0.7.1-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (456 kB)
Using cached idna-3.13-py3-none-any.whl (68 kB)
Using cached jinja2-3.1.6-py3-none-any.whl (134 kB)
Using cached jiter-0.14.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (358 kB)
Using cached orjson-3.11.9-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (133 kB)
Using cached pyasn1_modules-0.4.2-py3-none-any.whl (181 kB)
Using cached pyyaml-6.0.3-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (806 kB)
Using cached requests_oauthlib-2.0.0-py2.py3-none-any.whl (24 kB)
Using cached rsa-4.9.1-py3-none-any.whl (34 kB)
Using cached six-1.17.0-py2.py3-none-any.whl (11 kB)
Using cached soupsieve-2.8.3-py3-none-any.whl (37 kB)
Using cached starlette-0.37.2-py3-none-any.whl (71 kB)
Using cached tokenizers-0.23.1-cp310-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.3 MB)
Using cached typing_extensions-4.15.0-py3-none-any.whl (44 kB)
Using cached tzlocal-5.3.1-py3-none-any.whl (18 kB)
Using cached ujson-5.12.1-cp311-cp311-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (59 kB)
Using cached uritemplate-4.2.0-py3-none-any.whl (11 kB)
Using cached uvloop-0.22.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (3.8 MB)
Using cached watchfiles-1.1.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (456 kB)
Using cached websockets-16.0-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (184 kB)
Using cached certifi-2026.4.22-py3-none-any.whl (135 kB)
Using cached mako-1.3.12-py3-none-any.whl (78 kB)
Using cached pytz-2026.2-py2.py3-none-any.whl (510 kB)
Using cached sniffio-1.3.1-py3-none-any.whl (10 kB)
Using cached dnspython-2.8.0-py3-none-any.whl (331 kB)
Using cached googleapis_common_protos-1.75.0-py3-none-any.whl (300 kB)
Using cached huggingface_hub-1.14.0-py3-none-any.whl (661 kB)
Using cached markupsafe-3.0.3-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (22 kB)
Using cached oauthlib-3.3.1-py3-none-any.whl (160 kB)
Using cached proto_plus-1.28.0-py3-none-any.whl (50 kB)
Using cached protobuf-7.34.1-cp310-abi3-manylinux2014_x86_64.whl (324 kB)
Using cached pyasn1-0.6.3-py3-none-any.whl (83 kB)
Using cached pyparsing-3.3.2-py3-none-any.whl (122 kB)
Using cached requests-2.33.1-py3-none-any.whl (64 kB)
Using cached rich_toolkit-0.19.7-py3-none-any.whl (32 kB)
Using cached typer-0.25.1-py3-none-any.whl (58 kB)
Using cached annotated_doc-0.0.4-py3-none-any.whl (5.3 kB)
Using cached charset_normalizer-3.4.7-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (214 kB)
Using cached filelock-3.29.0-py3-none-any.whl (39 kB)
Using cached fsspec-2026.4.0-py3-none-any.whl (203 kB)
Using cached hf_xet-1.5.0-cp37-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (4.5 MB)
Using cached packaging-26.2-py3-none-any.whl (100 kB)
Using cached rich-15.0.0-py3-none-any.whl (310 kB)
Using cached shellingham-1.5.4-py2.py3-none-any.whl (9.8 kB)
Using cached tqdm-4.67.3-py3-none-any.whl (78 kB)
Using cached urllib3-2.7.0-py3-none-any.whl (131 kB)
Using cached markdown_it_py-4.2.0-py3-none-any.whl (91 kB)
Using cached pygments-2.20.0-py3-none-any.whl (1.2 MB)
Using cached mdurl-0.1.2-py3-none-any.whl (10.0 kB)
Installing collected packages: sgmllib3k, pytz, websockets, uvloop, urllib3, uritemplate, ujson, tzlocal, typing-extensions, tqdm, tenacity, soupsieve, sniffio, six, shellingham, pyyaml, python-multipart, python-dotenv, pyparsing, pygments, pyasn1, protobuf, packaging, orjson, oauthlib, mdurl, MarkupSafe, lxml, jiter, idna, httptools, hf-xet, h11, greenlet, fsspec, filelock, feedparser, dnspython, distro, click, charset_normalizer, certifi, cachetools, async-timeout, annotated-types, annotated-doc, aiofiles, uvicorn, sqlalchemy, rsa, requests, pydantic-core, pyasn1-modules, proto-plus, markdown-it-py, Mako, jinja2, httplib2, httpcore, googleapis-common-protos, email_validator, beautifulsoup4, asyncpg, apscheduler, anyio, watchfiles, starlette, rich, requests-oauthlib, pydantic, httpx, google-auth, alembic, typer, rich-toolkit, python-telegram-bot, pydantic-settings, notion-client, google-auth-oauthlib, google-auth-httplib2, google-api-core, huggingface-hub, google-api-python-client, fastapi-cli, tokenizers, fastapi, anthropic
Successfully installed Mako-1.3.12 MarkupSafe-3.0.3 aiofiles-23.2.1 alembic-1.13.1 annotated-doc-0.0.4 annotated-types-0.7.0 anthropic-0.26.1 anyio-4.13.0 apscheduler-3.10.4 async-timeout-5.0.1 asyncpg-0.29.0 beautifulsoup4-4.12.3 cachetools-5.5.2 certifi-2026.4.22 charset_normalizer-3.4.7 click-8.3.3 distro-1.9.0 dnspython-2.8.0 email_validator-2.3.0 fastapi-0.111.0 fastapi-cli-0.0.24 feedparser-6.0.11 filelock-3.29.0 fsspec-2026.4.0 google-api-core-2.30.3 google-api-python-client-2.129.0 google-auth-2.29.0 google-auth-httplib2-0.4.0 google-auth-oauthlib-1.2.0 googleapis-common-protos-1.75.0 greenlet-3.5.0 h11-0.16.0 hf-xet-1.5.0 httpcore-1.0.9 httplib2-0.31.2 httptools-0.7.1 httpx-0.27.0 huggingface-hub-1.14.0 idna-3.13 jinja2-3.1.6 jiter-0.14.0 lxml-5.2.2 markdown-it-py-4.2.0 mdurl-0.1.2 notion-client-2.2.1 oauthlib-3.3.1 orjson-3.11.9 packaging-26.2 proto-plus-1.28.0 protobuf-7.34.1 pyasn1-0.6.3 pyasn1-modules-0.4.2 pydantic-2.7.1 pydantic-core-2.18.2 pydantic-settings-2.2.1 pygments-2.20.0 pyparsing-3.3.2 python-dotenv-1.0.1 python-multipart-0.0.9 python-telegram-bot-21.3 pytz-2026.2 pyyaml-6.0.3 requests-2.33.1 requests-oauthlib-2.0.0 rich-15.0.0 rich-toolkit-0.19.7 rsa-4.9.1 sgmllib3k-1.0.0 shellingham-1.5.4 six-1.17.0 sniffio-1.3.1 soupsieve-2.8.3 sqlalchemy-2.0.30 starlette-0.37.2 tenacity-8.3.0 tokenizers-0.23.1 tqdm-4.67.3 typer-0.25.1 typing-extensions-4.15.0 tzlocal-5.3.1 ujson-5.12.1 uritemplate-4.2.0 urllib3-2.7.0 uvicorn-0.29.0 uvloop-0.22.1 watchfiles-1.1.1 websockets-16.0
[notice] A new release of pip is available: 24.0 -> 26.1.1
[notice] To update, run: pip install --upgrade pip
==> Uploading build...
==> Uploaded in 3.2s. Compression took 4.1s
==> Build successful 🎉
==> Deploying...
==> Setting WEB_CONCURRENCY=1 by default, based on available CPUs in the instance
==> Running 'uvicorn main:app --host 0.0.0.0 --port 10000'
INFO:     Started server process [58]
INFO:     Waiting for application startup.
ERROR:    Traceback (most recent call last):
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/starlette/routing.py", line 732, in lifespan
    async with self.lifespan_context(app) as maybe_state:
  File "/opt/render/project/python/Python-3.11.9/lib/python3.11/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/backend/main.py", line 21, in lifespan
    await init_db()
  File "/opt/render/project/src/backend/db/session.py", line 64, in init_db
    async with engine.begin() as conn:
  File "/opt/render/project/python/Python-3.11.9/lib/python3.11/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/sqlalchemy/ext/asyncio/engine.py", line 1063, in begin
    async with conn:
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/sqlalchemy/ext/asyncio/base.py", line 121, in __aenter__
    return await self.start(is_ctxmanager=True)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/sqlalchemy/ext/asyncio/engine.py", line 273, in start
    await greenlet_spawn(self.sync_engine.connect)
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 201, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3276, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 146, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 3300, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 449, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 1263, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 179, in _do_get
    with util.safe_reraise():
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
    return self._create_connection()
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 390, in _create_connection
    return _ConnectionRecord(self)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 674, in __init__
    self.__connect()
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 900, in __connect
    with util.safe_reraise():
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 146, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/sqlalchemy/pool/base.py", line 896, in __connect
    self.dbapi_connection = connection = pool._invoke_creator(self)
                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 643, in connect
    return dialect.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 620, in connect
    return self.loaded_dbapi.connect(*cargs, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 937, in connect
    await_only(creator_fn(*arg, **kw)),
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 131, in await_only
    return current.driver.switch(awaitable)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 196, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/asyncpg/connection.py", line 2329, in connect
    return await connect_utils._connect(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/asyncpg/connect_utils.py", line 1017, in _connect
    raise last_error or exceptions.TargetServerAttributeNotMatched(
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/asyncpg/connect_utils.py", line 991, in _connect
    conn = await _connect_addr(
           ^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/asyncpg/connect_utils.py", line 824, in _connect_addr
    return await __connect_addr(params, False, *args)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/asyncpg/connect_utils.py", line 873, in __connect_addr
    tr, pr = await connector
             ^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.11/site-packages/asyncpg/connect_utils.py", line 744, in _create_ssl_connection
Menu
    tr, pr = await loop.create_connection(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "uvloop/loop.pyx", line 1982, in create_connection
socket.gaierror: [Errno -2] Name or service not known
ERROR:    Application startup failed. Exiting.
==> Exited with status 3
==> Common ways to troubleshoot your deploy: https://render.com/docs/troubleshooting-deploys

---
INFO:     122.161.77.103:0 - "GET /api/v1/analytics/summary HTTP/1.1" 200 OK
2026-05-07 22:01:34,050 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-07 22:01:34,051 INFO sqlalchemy.engine.Engine SELECT applications.status, count(applications.id) AS count_1 
FROM applications GROUP BY applications.status
2026-05-07 22:01:34,051 INFO sqlalchemy.engine.Engine [cached since 28.81s ago] ()
2026-05-07 22:01:34,073 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-07 22:01:34,073 INFO sqlalchemy.engine.Engine SELECT jobs.id, jobs.title, jobs.company, jobs.location, jobs.url, jobs.source, jobs.description, jobs.required_skills, jobs.preferred_skills, jobs.experience_level, jobs.employment_type, jobs.salary_range, jobs.match_score, jobs.match_reasons, jobs.is_match, jobs.detected_at, jobs.created_at, jobs.updated_at 
FROM jobs 
WHERE jobs.is_match = true ORDER BY jobs.detected_at DESC 
 LIMIT $1::INTEGER OFFSET $2::INTEGER
2026-05-07 22:01:34,073 INFO sqlalchemy.engine.Engine [cached since 28.91s ago] (50, 0)
2026-05-07 22:01:34,075 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-07 22:01:34,076 INFO sqlalchemy.engine.Engine SELECT jobs.id, jobs.title, jobs.company, jobs.location, jobs.url, jobs.source, jobs.description, jobs.required_skills, jobs.preferred_skills, jobs.experience_level, jobs.employment_type, jobs.salary_range, jobs.match_score, jobs.match_reasons, jobs.is_match, jobs.detected_at, jobs.created_at, jobs.updated_at 
FROM jobs ORDER BY jobs.detected_at DESC 
 LIMIT $1::INTEGER OFFSET $2::INTEGER
2026-05-07 22:01:34,076 INFO sqlalchemy.engine.Engine [cached since 29.44s ago] (50, 0)
2026-05-07 22:01:34,238 INFO sqlalchemy.engine.Engine SELECT count(applications.id) AS count_1 
FROM applications 
WHERE applications.status = $1::VARCHAR
2026-05-07 22:01:34,238 INFO sqlalchemy.engine.Engine [cached since 28.81s ago] ('applied',)
2026-05-07 22:01:34,363 INFO sqlalchemy.engine.Engine SELECT count(applications.id) AS count_1 
FROM applications 
WHERE applications.status IN ($1::VARCHAR, $2::VARCHAR)
2026-05-07 22:01:34,363 INFO sqlalchemy.engine.Engine [cached since 28.8s ago] ('interviewing', 'offer')
2026-05-07 22:01:34,387 INFO sqlalchemy.engine.Engine ROLLBACK
INFO:     122.161.77.103:0 - "GET /api/v1/jobs?is_match=true HTTP/1.1" 200 OK
2026-05-07 22:01:34,488 INFO sqlalchemy.engine.Engine SELECT count(outreach_messages.id) AS count_1 
FROM outreach_messages 
WHERE outreach_messages.opened = true
2026-05-07 22:01:34,488 INFO sqlalchemy.engine.Engine [cached since 28.79s ago] ()
2026-05-07 22:01:34,523 INFO sqlalchemy.engine.Engine ROLLBACK
INFO:     122.161.77.103:0 - "GET /api/v1/jobs HTTP/1.1" 200 OK
2026-05-07 22:01:34,612 INFO sqlalchemy.engine.Engine SELECT count(outreach_messages.id) AS count_1 
FROM outreach_messages 
WHERE outreach_messages.sent = true
2026-05-07 22:01:34,612 INFO sqlalchemy.engine.Engine [cached since 28.79s ago] ()
2026-05-07 22:01:34,737 INFO sqlalchemy.engine.Engine SELECT jobs.company, avg(jobs.match_score) AS avg_score, count(jobs.id) AS count 
Menu
FROM jobs 
WHERE jobs.is_match = true GROUP BY jobs.company ORDER BY avg(jobs.match_score) DESC 
 LIMIT $1::INTEGER
2026-05-07 22:01:34,737 INFO sqlalchemy.engine.Engine [cached since 28.78s ago] (5,)
2026-05-07 22:01:34,862 INFO sqlalchemy.engine.Engine ROLLBACK
INFO:     122.161.77.103:0 - "GET /api/v1/analytics/summary HTTP/1.1" 200 OK
2026-05-07 22:01:58,031 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-05-07 22:01:58,031 INFO sqlalchemy.engine.Engine SELECT jobs.id, jobs.title, jobs.company, jobs.location, jobs.url, jobs.source, jobs.description, jobs.required_skills, jobs.preferred_skills, jobs.experience_level, jobs.employment_type, jobs.salary_range, jobs.match_score, jobs.match_reasons, jobs.is_match, jobs.detected_at, jobs.created_at, jobs.updated_at 
FROM jobs ORDER BY jobs.detected_at DESC 
 LIMIT $1::INTEGER OFFSET $2::INTEGER
2026-05-07 22:01:58,031 INFO sqlalchemy.engine.Engine [cached since 53.39s ago] (50, 0)
2026-05-07 22:01:58,409 INFO sqlalchemy.engine.Engine ROLLBACK
INFO:     122.161.77.103:0 - "GET /api/v1/jobs HTTP/1.1" 200 OK
---