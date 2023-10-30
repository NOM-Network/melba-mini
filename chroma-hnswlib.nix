{ lib
, stdenv
, buildPythonPackage
, fetchFromGitHub
, fetchPypi
, unittestCheckHook
, pythonOlder
, setuptools
, setuptools_scm
, pybind11
, numpy
}:

buildPythonPackage rec {
  pname = "chroma-hnswlib";
  version = "0.7.3";
  format = "pyproject";

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-thN77d5J//2mr5OwKX/gBCn8YeWgcrHtk3f5Ce2VqTI=";
  };

  buildInputs = [
    setuptools
    setuptools_scm
    pybind11
    numpy
  ];
}
