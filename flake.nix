{
  description = "melba-mini";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/c0c78361164a6601c8c0ce0b8560891f42c053f0";
    flake-utils.url = "github:numtide/flake-utils";
    llama-cpp.url = "github:shuni64/llama.cpp/e3932593d46c30145301a13097895f9376cba509";
    llama-cpp.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { self, nixpkgs, flake-utils, llama-cpp, ... }:
    flake-utils.lib.eachDefaultSystem (system: 
      let
        pkgs = import nixpkgs { inherit system; };
        llama = llama-cpp.packages.${system}.default;
        llama-cpp-python = pkgs.python3Packages.callPackage ./llama-cpp-python.nix { llama-cpp = llama; };
        chroma-hnswlib = pkgs.python3Packages.callPackage ./chroma-hnswlib.nix {};
        chromadb = pkgs.python3Packages.callPackage ./chromadb.nix { chroma-hnswlib = chroma-hnswlib; };
        textblob = pkgs.python3Packages.callPackage ./textblob.nix {};
        nrclex = pkgs.python3Packages.callPackage ./nrclex.nix { textblob = textblob; };
        websocketsNew = pkgs.python3Packages.callPackage ./websockets.nix {};
      in {
        devShell = pkgs.mkShell rec {
          stdenv = pkgs.clangStdenv;
          nativeBuildInputs = with pkgs; [
            (python3.withPackages(ps: with ps; [ llama-cpp-python chromadb nrclex websocketsNew ]))
          ];

          LLAMA_CPP_LIB = "${llama}/lib/libllama.so";
        };
    }
  );
}

