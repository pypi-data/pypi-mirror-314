# CHANGELOG


## v0.1.0-alpha.9 (2024-12-10)

### Bug Fixes

- **.dummy**: Force release of alpha
  ([`41dfb46`](https://github.com/populationgenomics/cpg-flow/commit/41dfb460d30c386ea82e6cb06cfebd2a982c1d5f))

### Build System

- **pyproject.toml,uv.lock**: Add networkx to core deps
  ([`e6a0826`](https://github.com/populationgenomics/cpg-flow/commit/e6a08265a18da34df9eb93a4db0b0ffd3ce24e8e))

- **uv.lock**: Bumped tornado dep
  ([`58a713f`](https://github.com/populationgenomics/cpg-flow/commit/58a713f25b3c4f6f7cd7be7ad59df2a1681e3029))

- **uv.lock,pyproject.toml**: Bumped grpcio dep
  ([`256552f`](https://github.com/populationgenomics/cpg-flow/commit/256552f31d32788a4bbcf1bab5b9392d3a9e37a6))

- **uv.lock,pyproject.toml,.github/workflows/security.yaml**: Bumped deps, improved security
  workflow
  ([`52449a8`](https://github.com/populationgenomics/cpg-flow/commit/52449a8cb05a5601fc859e19894e609e49902d6a))

- **Dockerfile**: Add explicit copying of deps files
  ([`693b3da`](https://github.com/populationgenomics/cpg-flow/commit/693b3daa4a11b68bc72a8ded3a7c550287442dda))

- **Dockerfile**: Fix typo in path
  ([`d181a83`](https://github.com/populationgenomics/cpg-flow/commit/d181a83b2ffdfb001f233b2852f601231b1a46e0))

- **Dockerfile,-tests/hail/workflow.py**: Force install of dev deps
  ([`10beaea`](https://github.com/populationgenomics/cpg-flow/commit/10beaeae82dbc461bce7c10f314c545716bc5622))

- **.dockerignore,-Dockerfile,-tests/hail/config.toml**: Improve uv setup in docker
  ([`652cbee`](https://github.com/populationgenomics/cpg-flow/commit/652cbeeb1cc0510b7110614b8cbfb04a719f8e36))

- **Dockerfile**: Activate venv in dockerfile
  ([`b086e9b`](https://github.com/populationgenomics/cpg-flow/commit/b086e9b54674ee378602249a0b7a0e86a4c56e01))

- **Dockerfile**: Uv sync after copying dir contents
  ([`2bb9dc8`](https://github.com/populationgenomics/cpg-flow/commit/2bb9dc8430602a92e258c4b64f14ec3c2d024c4e))

- **Dockerfile**: Use uv sync to install reqs
  ([`2ff5933`](https://github.com/populationgenomics/cpg-flow/commit/2ff59333f1b97132f17510e8a0f5d426189aa75a))

- **Dockerfile**: Test running uv from local bin
  ([`11b3477`](https://github.com/populationgenomics/cpg-flow/commit/11b3477af856bec94d2a50b5f06c85dff8f02dcf))

- **Dockerfile**: Adding source shell to Docker stage
  ([`4aa8e1f`](https://github.com/populationgenomics/cpg-flow/commit/4aa8e1f5cf0fba99dd0998c10a8bb01b04794297))

- **Dockerfile**: Test using uv docker img
  ([`6f2ec8f`](https://github.com/populationgenomics/cpg-flow/commit/6f2ec8fd4c34864fc35220e7a1660e7afa04473e))

- **Dockerfile**: Switch to uv and fix dir copy
  ([`b2db11d`](https://github.com/populationgenomics/cpg-flow/commit/b2db11d087e0a370bb4445fb8c8aa1de4d78048d))

### Code Style

- **.dummy**: Rm file
  ([`087f7d9`](https://github.com/populationgenomics/cpg-flow/commit/087f7d9f84b0c2c268a2af722ceee57fc6999cb3))

### Continuous Integration

- **hail.yaml**: Rm uneeded workflow
  ([`54ac1a9`](https://github.com/populationgenomics/cpg-flow/commit/54ac1a99731b3f2f7312086d66645eca1105329b))

- **.github/workflows/,tests/hail/**: Fix tests script again
  ([`03dd3a6`](https://github.com/populationgenomics/cpg-flow/commit/03dd3a651a849351dfc64927079aaa5ffffebdc1))

- **docker.yaml**: Fix build github sha
  ([`5cf3a7a`](https://github.com/populationgenomics/cpg-flow/commit/5cf3a7a7943e91aeed244396a384bcfff329cfad))

- **docker.yaml**: Echo sha
  ([`01f64d1`](https://github.com/populationgenomics/cpg-flow/commit/01f64d1e2052abeda3219d8d2de6c87cad6da4e2))

- **docker.yaml**: Fix push to images-tmp sha
  ([`df24a1e`](https://github.com/populationgenomics/cpg-flow/commit/df24a1e2141229becbe4f3a6a34ed2c8cc2c0e0f))

- **docker.yaml**: Change to $GITHUB_SHA
  ([`7d582c0`](https://github.com/populationgenomics/cpg-flow/commit/7d582c0c59f077565d70e577432afa93e08951ad))

- **manual-test.yaml**: Change to echo
  ([`0157daf`](https://github.com/populationgenomics/cpg-flow/commit/0157daf1b6b856931aa9d2abcf06207d042f9364))

- **manual-test.yaml**: Add a manual check for running workflow test
  ([`9a809cc`](https://github.com/populationgenomics/cpg-flow/commit/9a809ccc79188d412313239e5dc38ac737d27689))

- **.dummy**: Trigger commit docker build
  ([`d1e84bc`](https://github.com/populationgenomics/cpg-flow/commit/d1e84bcc2caaf4ec7eb54088f06793bc24826d66))

- **docker.yaml,pyproject.toml**: Get sem ver to update docker version
  ([`b0279b0`](https://github.com/populationgenomics/cpg-flow/commit/b0279b0cee7517ecbe5d66879f975d60b10457bb))

- **docker.yaml**: Push commit images to images-tmp
  ([`743a533`](https://github.com/populationgenomics/cpg-flow/commit/743a533fb28f7b8b657748b8184c01489e0b94d2))

- **docker.yaml**: Add push commit sha step
  ([`3d13938`](https://github.com/populationgenomics/cpg-flow/commit/3d1393817db9df8f01bd46219405975576fcaf7f))

- **.github/workflows/docker.yaml**: Added test environment
  ([`eff9cdc`](https://github.com/populationgenomics/cpg-flow/commit/eff9cdc1ecd3a0966c7e7ff4a6e3eee457e36b1f))

- **.github/workflows/renovate.yaml**: Removed input on workflow dispatch
  ([`aad0f9b`](https://github.com/populationgenomics/cpg-flow/commit/aad0f9bd4f3e3c14ca062012d76fc85c2ffe1196))

### Refactoring

- **.dummy**: Add dummy file
  ([`6317611`](https://github.com/populationgenomics/cpg-flow/commit/63176114962beefc3277701437e97eec57330dae))

- **tests/hail/**: Move to test_workflows_shared repo
  ([`c146832`](https://github.com/populationgenomics/cpg-flow/commit/c1468327bb71507d4ac89862266d307c4374515f))

### Testing

- **Dockerfile**: Add PYTHONPATH to Dockerfile
  ([`fddd50e`](https://github.com/populationgenomics/cpg-flow/commit/fddd50ef32f934e89f2ea4f43be85fe527c11004))

- **tests/hail/workflow.py**: Add import to run_cpg_flow
  ([`a48b8dc`](https://github.com/populationgenomics/cpg-flow/commit/a48b8dcedd7dda713fce5977e0f9f73de54c4a58))

- **tests/hail/workflow.py**: Revert stages import
  ([`d998be7`](https://github.com/populationgenomics/cpg-flow/commit/d998be748d36f5ffd6eb6aa83a09877ba483020b))

- **./,tests/hail/**: Make tests importable
  ([`7af791d`](https://github.com/populationgenomics/cpg-flow/commit/7af791dd249f29cce38b85abe7b2adac154265c0))

- **tests/hail/stages.py**: Fix?
  ([`765f65e`](https://github.com/populationgenomics/cpg-flow/commit/765f65ee83791b8e40c68165128ab156c1d96b04))

- **tests/hail/config.toml,tests/hail/stages.py**: Fix?
  ([`e113af2`](https://github.com/populationgenomics/cpg-flow/commit/e113af2f2bfef49260da7e44765b3a81bc95d47f))

- **tests/hail/stages.py**: Trying print dump in a python job
  ([`26a69d9`](https://github.com/populationgenomics/cpg-flow/commit/26a69d9fe6f46b33db81a5082398235f61bbb613))

- **tests/hail/stages.py**: Remove use of read_input for cumulative_calc
  ([`ada778e`](https://github.com/populationgenomics/cpg-flow/commit/ada778e85b629ab6ec679a34cbd4ec05941555e9))

- **tests/hail/stages.py**: Testing python jobs in stages
  ([`374c383`](https://github.com/populationgenomics/cpg-flow/commit/374c38397698204f84a6c53c474b2feb42206d99))

- **tests/hail/stages.py**: Testing python jobs within stages
  ([`5eeaa84`](https://github.com/populationgenomics/cpg-flow/commit/5eeaa84b38652c8a70ba24bb9b989fe257546883))

- **tests/hail/stages.py**: Removed single quote bug
  ([`30947c1`](https://github.com/populationgenomics/cpg-flow/commit/30947c178e67eb13e33dfe957d3c599e4e231dd0))

- **tests/hail/config.toml**: Remove local backend setting
  ([`9fdc5af`](https://github.com/populationgenomics/cpg-flow/commit/9fdc5af7adf1ed0759ecba051e718afba1c0cb2b))

- **tests/hail/workflow.py**: Temp removal of last 2 stages
  ([`c3d607d`](https://github.com/populationgenomics/cpg-flow/commit/c3d607d14793977345c97b63dbcbac54b6876fd5))

- **tests/hail/stage.py**: More testing
  ([`c044488`](https://github.com/populationgenomics/cpg-flow/commit/c044488333ed18f711e2c130273661585f1ada11))

- **tests/hail/stages.py**: Testing cumulative calc
  ([`af682c9`](https://github.com/populationgenomics/cpg-flow/commit/af682c9fcf2dd5fa0da95bb2be8d99e3e73da708))

- **tests/hail/*.py**: Added logging
  ([`03daed8`](https://github.com/populationgenomics/cpg-flow/commit/03daed807827c59aa30d9fba8e1f82bf30c31adf))

- **tests/hail/*.py**: Fix path reference for expected_outputs
  ([`31a14eb`](https://github.com/populationgenomics/cpg-flow/commit/31a14eba8b4c573847c0f7a8e2de19c5b35fd742))

- **tests/hail/workflow.py**: Better logging for config
  ([`b67dab4`](https://github.com/populationgenomics/cpg-flow/commit/b67dab4e0bec1df6b63606bd2294b6a91c7b492a))

- **tests/hail/workflow.py**: Fixed config compilation
  ([`20d56ce`](https://github.com/populationgenomics/cpg-flow/commit/20d56ceb528e2dc6652db27a13ed794943f443d7))

- **tests/hail/config.toml**: Added access_level and sequencing_type vars
  ([`5ec3812`](https://github.com/populationgenomics/cpg-flow/commit/5ec38124307e16a451989f141ac0a3c3e9e9bef0))

- **tests/hail/***: Fix linting, missing image arg to analysis-runner
  ([`7350986`](https://github.com/populationgenomics/cpg-flow/commit/735098694f1a2a1bc2be07aab38ff1ee9263637b))

- **tests/hail/workflow.py**: Standardise shebang
  ([`b405406`](https://github.com/populationgenomics/cpg-flow/commit/b4054060698dbb523165be9213227db7471079c8))

- **tests/hail/*.py,-Dockerfile**: Add explicit imports from src
  ([`ed0ddf3`](https://github.com/populationgenomics/cpg-flow/commit/ed0ddf3d8eb790d78575570d560b2b23e0662df0))

- **tests/hail/stages.py,tests/hail/workflow.py,Dockerfile**: Fixed some bugs, and refactored
  dockerfile for more accurate paths
  ([`41d86e6`](https://github.com/populationgenomics/cpg-flow/commit/41d86e62639b1752397e8f4eff220023a8ce55c3))

- **tests/hail/workflow.py**: Switch back shebang
  ([`71de065`](https://github.com/populationgenomics/cpg-flow/commit/71de0655a96362188184b32bdc2c251d8dcbc85b))

- **tests/hail/workflow.py**: Change shebang venv path
  ([`96c31b9`](https://github.com/populationgenomics/cpg-flow/commit/96c31b972c7390dd29b19ad02a54f5edfbbceb41))

- **tests/hail/run-test.sh**: Write better wait for docker loop
  ([`91a55ea`](https://github.com/populationgenomics/cpg-flow/commit/91a55ea459889b359f30e0e278e1f7f85f9dfe50))

- **tests/hail/run-test.sh**: Fix our script
  ([`3b9e782`](https://github.com/populationgenomics/cpg-flow/commit/3b9e78257cdaeed274b7469d927902b3e2af208d))

- **tests/hail/run-test.sh**: Check the image exists
  ([`8ea7013`](https://github.com/populationgenomics/cpg-flow/commit/8ea7013d35ef62ef10b32219bc24107fc93cec5e))

- **tests/hail/run-test.sh**: Check commit has pushed
  ([`191f4ca`](https://github.com/populationgenomics/cpg-flow/commit/191f4cacf8c96452442b4721c00c55239ad4e58b))

- **tests/hail/config.toml,tests/hail/run-test.sh**: Add warnings
  ([`12fa5bd`](https://github.com/populationgenomics/cpg-flow/commit/12fa5bd351a8f8344fc4f697c8bc71f328f48a25))

- **tests/hail/stages.py,tests/hail/workflow.py**: Complete workflow
  ([`2f63d3d`](https://github.com/populationgenomics/cpg-flow/commit/2f63d3d0d08ffed5eb5b3b58f5d44e0fb3135464))

- **.github/workflows/,tests/hail/**: Adding more to workflow test
  ([`eea12e7`](https://github.com/populationgenomics/cpg-flow/commit/eea12e7cd5e5c222f60056642b19d9868b430ac4))

- **tests/hail/**: Start writing cpg-flow workflow test
  ([`930790a`](https://github.com/populationgenomics/cpg-flow/commit/930790a89d9d0720c7def8eb2e4784ea17db1641))


## v0.1.0-alpha.8 (2024-11-15)

### Bug Fixes

- **package.yaml**: Fix setup step add git clone
  ([`21c1400`](https://github.com/populationgenomics/cpg-flow/commit/21c1400a6083df40dffa66b9a642bf3f7d8892f4))

- **package.yaml**: Remove redundant checkout step
  ([`0634f44`](https://github.com/populationgenomics/cpg-flow/commit/0634f445361bf050d6243d142411c8738601c9e7))

- **package.yaml**: Use github token in setup step
  ([`8601d62`](https://github.com/populationgenomics/cpg-flow/commit/8601d62983cdac7b6a70429ac1d1c1c0aa4cf0f2))

- **package.yaml**: Use bot token
  ([`99814f6`](https://github.com/populationgenomics/cpg-flow/commit/99814f61d5f91bed00c49bf954da4c13b247a574))

- **package.yaml**: Add verbose logging
  ([`6fca5fb`](https://github.com/populationgenomics/cpg-flow/commit/6fca5fb4688840f38322db90eafb8183b9f5b835))

- **pyproject.toml,uv.lock**: Rm unused dev
  ([`26c9361`](https://github.com/populationgenomics/cpg-flow/commit/26c93615ed4a53ca8c239f57d98b99666dcaf6c6))

- **package.yaml,pyproject.toml**: Add ignore token for push
  ([`517d522`](https://github.com/populationgenomics/cpg-flow/commit/517d522fdfad4c4042f0dd4a472655ff0697c4b9))

- **package.yaml**: Deploy key to exempt action from br protection rules
  ([`5683a10`](https://github.com/populationgenomics/cpg-flow/commit/5683a10b95daa9a772360d75912572cac8dc9c9e))

- **package.yaml**: Push to pypi not testpypi
  ([`3a59082`](https://github.com/populationgenomics/cpg-flow/commit/3a59082568d6cf2d4394714020c6eb7101ea8ba3))

### Chores

- Merge pull request #16 from populationgenomics/pypi-deploy
  ([`13a9f7d`](https://github.com/populationgenomics/cpg-flow/commit/13a9f7d737e1a73b86cca0c62c7c6c5c8aadf91a))

Pypi deploy

- Merge pull request #15 from populationgenomics/pypi-deploy
  ([`20b4886`](https://github.com/populationgenomics/cpg-flow/commit/20b48861685b2927186f69fa6338cec4eeb5f1c3))

fix(package.yaml): deploy key to exempt action from br protection rules

### Refactoring

- **.dummy**: Test token
  ([`fc48eb5`](https://github.com/populationgenomics/cpg-flow/commit/fc48eb52dcd4bc8a409cf229b7a9c2ed10288939))

- **.dummy**: Test token
  ([`ec00646`](https://github.com/populationgenomics/cpg-flow/commit/ec006467788e26482fd06c639c649c38feaae597))

- **.dummy**: Remove file, check token permissions
  ([`a5a36df`](https://github.com/populationgenomics/cpg-flow/commit/a5a36df0760595a421f606dae431ebfd770aa37f))

- **.dummy**: Test push to alpha using BOT_ACCESS_TOKEN
  ([`8284ac1`](https://github.com/populationgenomics/cpg-flow/commit/8284ac14890432ba0182aec0f2fb1feb2f41f278))


## v0.1.0-alpha.7 (2024-11-12)

### Bug Fixes

- **./,.github/workflows/**: Get package.yaml working
  ([`c1992f7`](https://github.com/populationgenomics/cpg-flow/commit/c1992f7595684e0c6ae4852358ae09526e557fe0))


## v0.1.0-alpha.6 (2024-11-12)

### Bug Fixes

- **Makefile,pyproject.toml**: Debug ci-build command
  ([`cdf2fcf`](https://github.com/populationgenomics/cpg-flow/commit/cdf2fcfe567ec0de7d7dc8fa3109cc6b28b744ad))

- **package.yaml,pyproject.toml**: Rm uv, base build with version fix
  ([`559d16b`](https://github.com/populationgenomics/cpg-flow/commit/559d16b10797927caee58cd1bf4245269271eac7))

- **package.yaml**: Add git auth
  ([`601669c`](https://github.com/populationgenomics/cpg-flow/commit/601669cbe7363dd56636d5ba96c345854e72e557))

- **package.yaml**: Fix package.yaml manual semantic command
  ([`f733c90`](https://github.com/populationgenomics/cpg-flow/commit/f733c90b050a012515284dc985d116b972744c71))

- **package.yaml,.pypirc**: Run semantic release manually
  ([`f872765`](https://github.com/populationgenomics/cpg-flow/commit/f8727656dd072635f87dde02f9b835cd9083c61b))

- **.dummy,package.yaml**: Trigger release, use venv in workflow
  ([`36a4057`](https://github.com/populationgenomics/cpg-flow/commit/36a405714c1eea6684c6308f001a7bbeddae0b31))

- **pyproject.toml**: Fix build command
  ([`37c43ec`](https://github.com/populationgenomics/cpg-flow/commit/37c43ec53d87948dc7db984d51d58dba92b1fafa))

- **./,.github/workflows/**: Fix package.yaml build command
  ([`e41138c`](https://github.com/populationgenomics/cpg-flow/commit/e41138c72fcf14bda795756f0c584f429cae37fd))

- **Makefile,pyproject.toml**: Update build system
  ([`759ef2d`](https://github.com/populationgenomics/cpg-flow/commit/759ef2dcacee15050d49fe006ff3f4815375f1b3))


## v0.1.0-alpha.5 (2024-11-12)

### Bug Fixes

- **.dummy**: Fix forces a release
  ([`6e34931`](https://github.com/populationgenomics/cpg-flow/commit/6e349310bf2b470952bcedcce28b47ae01cb8d8d))

### Build System

- **pyproject.toml**: Fix project version
  ([`ddac37c`](https://github.com/populationgenomics/cpg-flow/commit/ddac37c3e53afd0a69b1f63abccb2cf239a36ec3))


## v0.1.0-alpha.4 (2024-11-12)

### Bug Fixes

- **pyproject.toml**: Remove dynamic version
  ([`4dcc2b9`](https://github.com/populationgenomics/cpg-flow/commit/4dcc2b9aa219c9a2e3ba041db71f20800c5b17a6))

- **pyproject.toml**: Remove dynamic version
  ([`9beca1f`](https://github.com/populationgenomics/cpg-flow/commit/9beca1fa8d22edf373b998c7e6cddcfb41c5e11a))


## v0.1.0-alpha.3 (2024-11-12)

### Bug Fixes

- **.dummy**: Fix commit to trigger release
  ([`e8a15a1`](https://github.com/populationgenomics/cpg-flow/commit/e8a15a1a2c5eec19c656a1832338ff736208db14))

### Continuous Integration

- **package.yaml**: Add verbose to pypi upload
  ([`a431fa6`](https://github.com/populationgenomics/cpg-flow/commit/a431fa67a09e41a2f2527a128d264dfb007411ba))


## v0.1.0-alpha.2 (2024-11-12)

### Bug Fixes

- **.dummy**: Add dummy file to trigger fix change
  ([`83546d3`](https://github.com/populationgenomics/cpg-flow/commit/83546d3d19108a9f089379e61e6de03b14002f7f))

### Continuous Integration

- **package.yaml**: Add contents write to package workflow
  ([`366efd1`](https://github.com/populationgenomics/cpg-flow/commit/366efd1896d9142beb23c2cb4f59aef4add35bc8))

- **package.yaml**: Upload to testpypi and fix gh permissions
  ([`0a253d3`](https://github.com/populationgenomics/cpg-flow/commit/0a253d3499729a788bc047edbe32bc0d3b75bab1))


## v0.1.0-alpha.1 (2024-11-12)

### Bug Fixes

- **src/cpg_flow/,tests/,tests/assets/**: Debugging test_cohort.py
  ([`238ab67`](https://github.com/populationgenomics/cpg-flow/commit/238ab67fb36ce771d4efef9898180cab1a7ff026))

- **tests/,tests/assets/,tests/stages/**: Fix test mocks and files
  ([`aae8755`](https://github.com/populationgenomics/cpg-flow/commit/aae87550ff1b6f410a6b3d193079b3a8b40171c4))

- **tests/stages/__init__.py**: Fix file to prod-pipes #959 version
  ([`91b875e`](https://github.com/populationgenomics/cpg-flow/commit/91b875ebebc9251a8b435ef34996b82bc76b5896))

- Rename cpg_workflow to cpg_flow
  ([`b387b3c`](https://github.com/populationgenomics/cpg-flow/commit/b387b3c1ff6d9ac1726b50e52ddca00abc2522e9))

- **workflow.py**: Fix circular import error
  ([`8de184f`](https://github.com/populationgenomics/cpg-flow/commit/8de184fa88db81aee52ba3c5ebcc7b3f646f2907))

- **src/cpg_flow/targets/**: Fix circular import issue
  ([`ca793b1`](https://github.com/populationgenomics/cpg-flow/commit/ca793b1af01d568b3058abfce1b2431c9b7f3c66))

- **pyproject.toml**: Switch back to 3.10 for prod pipes, add deps fix
  ([`1a0e214`](https://github.com/populationgenomics/cpg-flow/commit/1a0e2144901697029f1196cc8bedc9ab7979542e))

- **test.yaml**: Fix path to tests folder
  ([`199b168`](https://github.com/populationgenomics/cpg-flow/commit/199b1684974159b7afa1b5c6e33decdecaad4505))

- **test.yaml**: Revert to 3.10
  ([`69e4f14`](https://github.com/populationgenomics/cpg-flow/commit/69e4f14d8f9dd1341021ce6ddad1a30542797ef5))

### Build System

- **.github/renovate-config.json**: Removed merge commit msg debris
  ([`3f845a1`](https://github.com/populationgenomics/cpg-flow/commit/3f845a16fb849e3979ece711f1040ffe22f47866))

- **.github/workflows/renovate.yaml**: Attempting to fix the code checkout
  ([`3f326ba`](https://github.com/populationgenomics/cpg-flow/commit/3f326baf904b1226bcc36454e4afefff5ab48903))

- **.github/workflows/renovate.yaml**: Fix how the workflow dispatch call works
  ([`8190250`](https://github.com/populationgenomics/cpg-flow/commit/8190250a39ff05b9b1135ad8f7310722d7848f79))

- **requirements/***: Potential fix to renovatebot detecting deps
  ([`afaafd3`](https://github.com/populationgenomics/cpg-flow/commit/afaafd3eefd20cff9078fecb88cbbcbc0bb531a6))

- **pyproject.toml**: Allow chore tag option
  ([`a85e24b`](https://github.com/populationgenomics/cpg-flow/commit/a85e24b7b8fe1f5034f0b65df8f228b7650b4a23))

- **pyproject.toml,uv.lock**: Add commitizen to dev deps, rm old ones
  ([`17cf760`](https://github.com/populationgenomics/cpg-flow/commit/17cf760fe81f70002786af88adee129ca8503db0))

- **pyproject.toml,uv.lock**: Add pytest_mock
  ([`b6de677`](https://github.com/populationgenomics/cpg-flow/commit/b6de67747a16c199836457cbc54e34243a90db14))

- **pyproject.toml**: Remove unused mypy options
  ([`61147e5`](https://github.com/populationgenomics/cpg-flow/commit/61147e563953eb01c156d70b161a629cc6245092))

- **pyproject.toml**: Setup ruff linting and ruff isort configs, black config
  ([`1c769f8`](https://github.com/populationgenomics/cpg-flow/commit/1c769f8795e76bdd763b6d7a707245758bf421d2))

- **Dockerfile**: Added a skeleton Dockerfile
  ([`b2ee7bb`](https://github.com/populationgenomics/cpg-flow/commit/b2ee7bb89c530060b09f94538b4b0f8181c7865b))

- **pyproject.toml**: Bumped hail to 0.2.133
  ([`785adb5`](https://github.com/populationgenomics/cpg-flow/commit/785adb56be57d322afc7b6fc34d867c9d771cb93))

- **.github/workflows/renovate.yaml**: Fix how the workflow dispatch call works
  ([#11](https://github.com/populationgenomics/cpg-flow/pull/11),
  [`951c3b0`](https://github.com/populationgenomics/cpg-flow/commit/951c3b0a711c2d1f1d4582f7871f7b743f17bb86))

- **Makefile,README.md**: Update dev instructions and init in Makefile
  ([`ff111d8`](https://github.com/populationgenomics/cpg-flow/commit/ff111d831c4aa3527fe47bc9d38b14988dcabd24))

- **test.yaml**: Disable test workflow for now
  ([`3574ea2`](https://github.com/populationgenomics/cpg-flow/commit/3574ea2621cd5b23f1214ca0740d9e3cabbea8cc))

- **pre-commit**: Add commitlint
  ([`09c6915`](https://github.com/populationgenomics/cpg-flow/commit/09c691512273b6ebd519c83da756f4dd0fffe096))

- **Makefile**: Create makefile for building and installing dependencies
  ([`b8ab07b`](https://github.com/populationgenomics/cpg-flow/commit/b8ab07bc6133a054bb9ed531fc055fc0f31f3a90))

### Chores

- Merge migration-integration into migration-03
  ([`a2054ef`](https://github.com/populationgenomics/cpg-flow/commit/a2054ef04201ce36647f61bd9a5fa47a2c383bb5))

- Merge remote
  ([`10149d5`](https://github.com/populationgenomics/cpg-flow/commit/10149d58a66244a30390065c250c1c083fbb34f8))

- Merge main
  ([`0fb19d8`](https://github.com/populationgenomics/cpg-flow/commit/0fb19d8a3b512367c2f0f131244510e271a66006))

### Code Style

- **pyproject.toml**: Removed black and isort config, added additional ignore to ruff
  ([`5b550ee`](https://github.com/populationgenomics/cpg-flow/commit/5b550eea3510df7394f8c05d2724953cf94dd100))

- **.pre-commit-config.yaml,-src/***: Better linting, removed black and isort from pre-commit
  ([`4f05eb1`](https://github.com/populationgenomics/cpg-flow/commit/4f05eb1ddafb6c61aa2eac0752eb909ecac2670a))

- **README**: Fix title links
  ([`54e8031`](https://github.com/populationgenomics/cpg-flow/commit/54e8031cbb82b252a016d5a3a19cf6ab24e85388))

### Continuous Integration

- **.github/workflows/renovate.yaml,-uv.lock**: Removed push calls to the workflow
  ([`cbb5004`](https://github.com/populationgenomics/cpg-flow/commit/cbb50049d508b4997333feb909f8c92cd876032f))

- **.github/renovate-config.json**: Selected alpha as the target branch, and switched to uv
  ([`f434110`](https://github.com/populationgenomics/cpg-flow/commit/f4341108fd87ed287a857b9c487d494e38afe1f5))

- **.github/renovate-config.json**: Use uv to manage deps
  ([`9724557`](https://github.com/populationgenomics/cpg-flow/commit/9724557eca258bb669bb0efdc1551d2700c9a851))

- **package.yaml,pyproject.toml**: Modify semantic release build command
  ([`b990638`](https://github.com/populationgenomics/cpg-flow/commit/b9906386085aed7c985332eee4360f468ce99ccf))

- **package.yaml**: Add fetch-depth 0
  ([`b1500fe`](https://github.com/populationgenomics/cpg-flow/commit/b1500fef2d13444ba73b924bdb260e4886df648d))

- **package.yaml**: Fix publish action version
  ([`c17bc5e`](https://github.com/populationgenomics/cpg-flow/commit/c17bc5e160177ed132a1dbd69dabfb306c967de1))

- **package.yaml**: Trigger package on push just for testing
  ([`1de648f`](https://github.com/populationgenomics/cpg-flow/commit/1de648f8244eed2b209d42f8d55f9ade14168347))

- **package.yaml**: Remove dependent steps
  ([`aa42e8f`](https://github.com/populationgenomics/cpg-flow/commit/aa42e8ff7cc30ff60eafa6df1e0253cb0f575a16))

- **lint.yaml,test.yaml**: Rm on pull_request for test and lint
  ([`0e6a5e6`](https://github.com/populationgenomics/cpg-flow/commit/0e6a5e6484a8a7bf505f5f4e123ef7f1df85c8db))

- **security.yaml**: Fix security.yaml
  ([`70fffb1`](https://github.com/populationgenomics/cpg-flow/commit/70fffb1fd9178b7c1d0b64adb01abe858b4f46af))

- **package.yaml,pyproject.toml**: Setup package.yaml workflow
  ([`89694c2`](https://github.com/populationgenomics/cpg-flow/commit/89694c21df57222d6fd19130c9733e2f02be7ee0))

- **package.yaml,test.yaml-,+6**: Debugging package.yaml
  ([`0cf28cc`](https://github.com/populationgenomics/cpg-flow/commit/0cf28cccf7ae64c75f32f0e8a57c28e2b65ff9c6))

- **./,.github/workflows/**: Fix workflows, pin python version
  ([`a9c91fb`](https://github.com/populationgenomics/cpg-flow/commit/a9c91fb03065686afd9f16f87360f3521e8cf257))

- **lint.yaml**: Fix lint.yaml
  ([`55b6df4`](https://github.com/populationgenomics/cpg-flow/commit/55b6df42d0620301dc1c34b065ebc5956f1a3f37))

- **test.yaml**: Fix test.yaml workflow
  ([`e382488`](https://github.com/populationgenomics/cpg-flow/commit/e38248833c3341182f5293fc31d4f3355a802698))

- **test.yaml,.gitignore-,+7**: Fixing test.yaml
  ([`b5f3bac`](https://github.com/populationgenomics/cpg-flow/commit/b5f3bac958de1c9f200a9ca023bb7a042698de46))

- **.github/workflows/security.yaml**: Fixed requirements path
  ([`4a1ae56`](https://github.com/populationgenomics/cpg-flow/commit/4a1ae562dbc4600b717379befc269817d604acec))

- **security.yaml**: Add pip-audit workflow
  ([`8d6ad9e`](https://github.com/populationgenomics/cpg-flow/commit/8d6ad9ecfe2ac4a130fdc1129b358da71f774569))

PR: #909 from production-pipelines

- **.github/workflows/docker.yaml**: Added a docker workflow that builds and pushes a docker image
  ([`4b02ff1`](https://github.com/populationgenomics/cpg-flow/commit/4b02ff11ee2baad93d717ea28bfff940d2482932))

- **.github/workflows/package.yaml**: Changed the package name to cpg_flow
  ([`2e54fb9`](https://github.com/populationgenomics/cpg-flow/commit/2e54fb9f41d69e39016e97afc2e1d605874317af))

- **.github/workflows/lint.yaml**: Added additional triggers
  ([`e0eb58e`](https://github.com/populationgenomics/cpg-flow/commit/e0eb58e31ce9ef226ee9877b75204ef7f65fa564))

### Documentation

- **src/cpg_flow/targets/dataset.py**: Added better docs about the file
  ([`bee79ba`](https://github.com/populationgenomics/cpg-flow/commit/bee79bafc1978df0d364e32fe221d9bf87736dd5))

- **DEVELOPERS.md**: Updated dev setup instructions and Python versions
  ([`a4148ea`](https://github.com/populationgenomics/cpg-flow/commit/a4148ead36654538d093c60013de76164fe4cd01))

- **tests/README.md**: Remove keep tags
  ([`2835445`](https://github.com/populationgenomics/cpg-flow/commit/283544543ee110d778ccbec6b2da9467d7a9491f))

- **tests/README.md**: Move readme from prod pipes
  ([`ecbce2d`](https://github.com/populationgenomics/cpg-flow/commit/ecbce2d8a175b55d9ede8d8d9d427467b910f6a3))

### Features

- **Makefile,pyproject.toml,workflows**: Upgrad to using uv
  ([`02a946d`](https://github.com/populationgenomics/cpg-flow/commit/02a946dfc6cda94f185423ee00b18268a1720133))

### Refactoring

- **misc/attach_disk_test.py**: Remove file
  ([`807d886`](https://github.com/populationgenomics/cpg-flow/commit/807d886f99659c163e80e60574072e60df3b25eb))

PR#6: See Matt's comment

- **src/cpg_flow**: Removed some unused code and added better docs
  ([`cb64bf6`](https://github.com/populationgenomics/cpg-flow/commit/cb64bf649861a31eadeb306246b57ff0c3f4aad8))

- **src/cpg_flow/inputs.py**: Refactor to remove infinite loop, and cleanup
  ([`06591c5`](https://github.com/populationgenomics/cpg-flow/commit/06591c52e16ca2f9178aa05ec356f9609be76415))

- **src/cpg_flow**: Moved more stages out of the workflow file
  ([`9f67ab4`](https://github.com/populationgenomics/cpg-flow/commit/9f67ab47462932ba3e4f403e2a086ba02ac23918))

- **src/cpg_flow/targets**: Switched filenames to snake case and refactored linting
  ([`4345a82`](https://github.com/populationgenomics/cpg-flow/commit/4345a82c826b88cb0ff2e7be159fd6b2ac779c4a))

- **src/cpg_flow/defaults.toml**: Removed unused configs
  ([`fba83dc`](https://github.com/populationgenomics/cpg-flow/commit/fba83dceb9ce7be3339234db7b5da62d82bd748f))

- **src/cpg_flow/inputs.py**: Removed dead code and fixed some method calls
  ([`49e70a3`](https://github.com/populationgenomics/cpg-flow/commit/49e70a3e4e2857e50f07fbc09c4ceb56bb9d9e79))

Migration from production-pipelines

- **src/cpg_flow**: Fixed imports from targets
  ([`2d8348b`](https://github.com/populationgenomics/cpg-flow/commit/2d8348b7f43b05a78e2f1e521b1a1daa6d271037))

- **resources.py**: Migrate file, remove one unused section
  ([`38c3c9e`](https://github.com/populationgenomics/cpg-flow/commit/38c3c9e4e7a616395327e003f96c0b53394073dd))

- **cpg_flow/targets/**: Add init file and simplify imports
  ([`89fe513`](https://github.com/populationgenomics/cpg-flow/commit/89fe513a65e504ca51f9d26cc8fdbdc2c959d491))

- **utils.py**: Move cpg_workflows/batch.py into utils
  ([`28733a5`](https://github.com/populationgenomics/cpg-flow/commit/28733a52e35f1e033cb4b52e1f0a247704fa7f1a))

- **cpg_flow/targets/**: Add targets.py file, split by class
  ([`39db87c`](https://github.com/populationgenomics/cpg-flow/commit/39db87cd3d6d9c77b01fc2bb0d0cb9d5a6972831))

- **src/cpg_flow/metamist.py**: Removed dead code that we no longer needed
  ([`3d54754`](https://github.com/populationgenomics/cpg-flow/commit/3d54754f038ea358c5d6e2bd790114d31f1ebc4a))

Migration from production-pipelines

- **src/cpg_flow/workflow.py**: Removed the Stage class and other related classes from this file
  ([`941272d`](https://github.com/populationgenomics/cpg-flow/commit/941272dd58d4781c6ca85b3d7b1f85cec1125d1b))

- **src/cpg_flow/stage.py**: Split the Stage class into its own file
  ([`4dad84e`](https://github.com/populationgenomics/cpg-flow/commit/4dad84e738529bf46a5eb50eb4ddec4b02499100))

Migration from production-pipelines

- **cpg_flow/status.py**: Migrate the whole file
  ([`771b767`](https://github.com/populationgenomics/cpg-flow/commit/771b767226cd8cd5e3b0333f2e5f4fc14b187c45))

- **cpg_flow/defaults.toml**: Migrate the whole file
  ([`8c36fd4`](https://github.com/populationgenomics/cpg-flow/commit/8c36fd4ceae1680d20da7a4c996356c644f48e58))

- **cpg_flow/utils.py**: Migrate the whole file
  ([`8345483`](https://github.com/populationgenomics/cpg-flow/commit/8345483a30bcaed20a374b16d479f075f100de79))

- **cpg_flow/filetypes.py**: Migrate file, update deps
  ([`1f9406d`](https://github.com/populationgenomics/cpg-flow/commit/1f9406d60c059eb248585ccb3f18c5eaf48b94a8))

- **test/__init__.py**: Move to new tests folder
  ([`74d1f18`](https://github.com/populationgenomics/cpg-flow/commit/74d1f187e01753a6e6718c28f1cd4a81717c0cf7))

- **.files,-pyproject.toml,-__init__.py,-README.md**: Added config files and update to readme
  ([`1fd7ae6`](https://github.com/populationgenomics/cpg-flow/commit/1fd7ae69dfafc6a58435723d14a4a452822d5e0a))

### Testing

- **tests/,tests/assets/test_cohort/**: Refactor test_cohort.py
  ([`e4dca3f`](https://github.com/populationgenomics/cpg-flow/commit/e4dca3f5a7068b1fa5ea773ec4ed8d0b51588e20))

- **src/cpg_flow/,tests/**: Fix tests in cpg flow
  ([`0682555`](https://github.com/populationgenomics/cpg-flow/commit/0682555ba66479d7f1ed0358da726a862a45a7d4))

- **tests/conftest.py**: Add conftest to try to get tests working
  ([`d8e6d64`](https://github.com/populationgenomics/cpg-flow/commit/d8e6d64c1500dcd8f6d9dcb1e902971005676450))

- **test.yaml,src/cpg_flow/inputs.py-,+4**: Fix cpg-flow tests, try ci
  ([`aadef8b`](https://github.com/populationgenomics/cpg-flow/commit/aadef8b2882f0d8b0b94cb04f4c4d5a1b5def2ce))

- **tests/test_workflow.py**: Add test, cpg_workflow -> cpg_flow
  ([`6028ef0`](https://github.com/populationgenomics/cpg-flow/commit/6028ef0861cf7b07f03aab8aaeed00f45bcc6811))

- **cpg_flow/__init__.py,test_status.py**: Add test, fix stage imports
  ([`ec45f3b`](https://github.com/populationgenomics/cpg-flow/commit/ec45f3b18c18c6944827723c2f137253049d5f96))

- **tests/test_multicohort.py**: Add test, cpg_workflow -> cpg_flow
  ([`b28140d`](https://github.com/populationgenomics/cpg-flow/commit/b28140df021ccf060938b9668da90aa1df258b45))

- **tests/test_cohort.py**: Add test, cpg_workflow -> cpg_flow
  ([`e78f1f4`](https://github.com/populationgenomics/cpg-flow/commit/e78f1f427bd1b2aed6769d60ef3a9808682102eb))

- **test_metamist.py**: Add test, remove unused import, fix deps
  ([`bf4dbe4`](https://github.com/populationgenomics/cpg-flow/commit/bf4dbe42bac5afc062b6fb67a7e9990ad1cbd206))

- **test_stage_types.py**: Add test, add helper functions
  ([`ff6eb2c`](https://github.com/populationgenomics/cpg-flow/commit/ff6eb2cd1225c9e6cb3e51ccb2fddb938984be37))

- **test_skip_stages.py**: Add test
  ([`bc665da`](https://github.com/populationgenomics/cpg-flow/commit/bc665dacc68a0d2446ed37134a6d3077bba59abd))

- **test_skip_stages_fail.py**: Add test
  ([`108b52e`](https://github.com/populationgenomics/cpg-flow/commit/108b52edac54f92374e5b1e537c43eb8507e57d9))

- **test_only_stages.py**: Add test
  ([`8fe01dc`](https://github.com/populationgenomics/cpg-flow/commit/8fe01dc3b7edf094b9adabb1c02173f6c81e2b2a))

- **test_last_stages.py**: Add test
  ([`63ebc43`](https://github.com/populationgenomics/cpg-flow/commit/63ebc436ad29cd36403f3c34c017f527c5de67d5))

- **test_force_stages.py**: Add test
  ([`9cc2a54`](https://github.com/populationgenomics/cpg-flow/commit/9cc2a5459c4f55fc8dc5f7995be64d0fb5ba1592))

- **test_first_last_stages.py**: Add test
  ([`9e9870d`](https://github.com/populationgenomics/cpg-flow/commit/9e9870decd8aa7d24d2b2ffce00e0204eb98fb2f))

- **src/cpg_flow/,tests/**: Fix imports, add test first last stage
  ([`0501661`](https://github.com/populationgenomics/cpg-flow/commit/05016612cd9c0fc6f2c63aa4cf498b35bce7195f))

- **test/stages/__init__.py**: Copy over test stages init
  ([`8636c6d`](https://github.com/populationgenomics/cpg-flow/commit/8636c6da5b28c52f959f2c4dd8399af8a82fa6ab))

- **test/__init__.py**: Moved from production-pipelines
  ([`49ee73b`](https://github.com/populationgenomics/cpg-flow/commit/49ee73b0903c383da51faadd6df10c1ab4230746))

- **misc/attach_disk_test.py**: Moved from production-pipelines
  ([`38ab29a`](https://github.com/populationgenomics/cpg-flow/commit/38ab29a2bdc3b494f0a4f124f729ff7cc3504ef1))
