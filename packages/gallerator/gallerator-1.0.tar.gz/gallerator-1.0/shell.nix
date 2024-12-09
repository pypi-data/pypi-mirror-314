# This works with direnv:
#
# nix shell nixpkgs#{nix-direnv,direnv}
#
# and then enter this directory
#
# Automatic environment activation with direnv — nix.dev documentation
# https://nix.dev/guides/recipes/direnv.html

let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-23.11";
  pkgs = import nixpkgs { config = {}; overlays = []; };
  PROJECT_ROOT = builtins.toString ./.;

in


pkgs.mkShellNoCC {
  packages = with pkgs; [
    python312
    sqlite
    libGL
    ffmpeg
    file
    entr
    nodejs
  ];

  shellHook = ''
  . ${PROJECT_ROOT}/venv/bin/activate
  # This is setup by Makefile by creating a .pth file under venv/
  PYTHONPATH=$PYTHONPATH:${PROJECT_ROOT}/src
  '';
}

# Now you can `gallerator --help` and it works
