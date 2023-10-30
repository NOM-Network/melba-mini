{ lib
, stdenv
, buildPythonPackage
, fetchFromGitHub
, unittestCheckHook
, pythonOlder
, scikit-build-core
, pyproject-metadata
, pathspec
, cmake
, ninja
, llama-cpp
, diskcache
, typing-extensions
, numpy
}:

buildPythonPackage rec {
  pname = "llama-cpp-python";
  version = "0.2.12-git";
  format = "pyproject";

  LLAMA_BUILD = "OFF";
  dontUseCmakeConfigure = true;
  pypaBuildFlags = [ "--skip-dependency-check" "--config-setting=cmake.define.LLAMA_BUILD=OFF" ];

  src = fetchFromGitHub {
    owner = "abetlen";
    repo = pname;
    rev = "53861c9e530c74579c72e0426b0556bc8ad3f58b";
    hash = "sha256-hILmlJgb50rRMRWXZWPWTBZjq0l3f6EbGX5zsBPsSVc=";
  };

  nativeBuildInputs = [
    cmake
    ninja
  ];

  buildInputs = [
    scikit-build-core
    pyproject-metadata
    pathspec
  ];

  propagatedBuildInputs = [
    diskcache
    typing-extensions
    numpy
  ];
}
