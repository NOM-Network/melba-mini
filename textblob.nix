{ lib
, stdenv
, buildPythonPackage
, fetchFromGitHub
, fetchPypi
, unittestCheckHook
, pythonOlder
, nltk
}:

buildPythonPackage rec {
  pname = "textblob";
  version = "0.17.1";
  format = "setuptools";

  src = fetchFromGitHub {
    owner = "sloria";
    repo = "TextBlob";
    rev = "refs/tags/${version}";
    hash = "sha256-2/Q3xCeyzSeVDtIxw4HtqPeFXBYtsUvEr3UUF4BsvHo=";
  };

  propagatedBuildInputs = [
    nltk
  ];

  doCheck = false;
}
