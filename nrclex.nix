{ lib
, stdenv
, buildPythonPackage
, fetchFromGitHub
, fetchPypi
, unittestCheckHook
, pythonOlder
, textblob
}:

buildPythonPackage rec {
  pname = "nrclex";
  version = "3.0.0";
  format = "setuptools";

  src = fetchFromGitHub {
    owner = "metalcorebear";
    repo = "nrclex";
    rev = "5d66076ad897a2c9406d6c2a3b3d7b7cb3b25644";
    hash = "sha256-IWyWe50uYIvjhv5inqA74ygFr5/F17pCao92BhcPmsk=";
  };

  propagatedBuildInputs = [
    textblob
  ];

  doCheck = false;
}
