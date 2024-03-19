let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  buildInputs = [
    (import ./fplan.nix { })
  ];
  packages = [
    (pkgs.python3.withPackages (python-pkgs: [
      python-pkgs.scipy
    ]))
  ];
}
