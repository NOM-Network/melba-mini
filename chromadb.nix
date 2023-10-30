{ lib
, stdenv
, buildPythonPackage
, fetchFromGitHub
, fetchPypi
, unittestCheckHook
, pythonOlder
, setuptools
, setuptools_scm
, overrides
, pydantic
, requests
, onnxruntime
, tokenizers
, tqdm
, posthog
, importlib-resources
, pypika
, chroma-hnswlib
}:

buildPythonPackage rec {
  pname = "chromadb";
  version = "0.4.14";
  format = "pyproject";

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-D872A7z5yFQwUCDD+NNowJsVRdSL0rzu/VGGEJD4fa0=";
  };

  buildInputs = [
    setuptools
    setuptools_scm
  ];

  propagatedBuildInputs = [
    overrides
    pydantic
    requests
    onnxruntime
    tokenizers
    tqdm
    posthog
    importlib-resources
    pypika
    chroma-hnswlib
  ];
}
