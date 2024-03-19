{ pkgs ? import <nixpkgs> {}, ... }:

let
  pypkgs = pkgs.python311Packages;
in
pypkgs.buildPythonApplication rec {
    pname = "fplan";
    version = "0.0.1";

    src = pkgs.fetchFromGitHub {
        owner = "wscott";
        repo = "fplan";
        rev = "fac4b7b1d5bb37bc7451b263d82b2f716488d99b";
        sha256 = "HoDawwRNdbc5h64Rqsc78/CXdsyg9lB+obh3auziJho=";
    };

    sourceRoot = "${src.name}";
    format = "pyproject";

    propagatedBuildInputs = [ pypkgs.scipy pypkgs.hatchling ];
    doCheck = false;
}
