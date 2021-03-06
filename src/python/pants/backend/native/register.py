# coding=utf-8
# Copyright 2018 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

from pants.backend.native.config.environment import create_native_environment_rules
from pants.backend.native.subsystems.binaries.binutils import create_binutils_rules
from pants.backend.native.subsystems.binaries.gcc import create_gcc_rules
from pants.backend.native.subsystems.binaries.llvm import create_llvm_rules
from pants.backend.native.subsystems.native_toolchain import create_native_toolchain_rules
from pants.backend.native.subsystems.xcode_cli_tools import create_xcode_cli_tools_rules
from pants.backend.native.targets.native_artifact import NativeArtifact
from pants.backend.native.targets.native_library import CLibrary, CppLibrary
from pants.backend.native.tasks.c_compile import CCompile
from pants.backend.native.tasks.cpp_compile import CppCompile
from pants.backend.native.tasks.link_shared_libraries import LinkSharedLibraries
from pants.build_graph.build_file_aliases import BuildFileAliases
from pants.goal.task_registrar import TaskRegistrar as task


def build_file_aliases():
  return BuildFileAliases(
    targets={
      CLibrary.alias(): CLibrary,
      CppLibrary.alias(): CppLibrary,
    },
    objects={
      NativeArtifact.alias(): NativeArtifact,
    }
  )


def register_goals():
  # FIXME(#5962): register these under the 'compile' goal when we eliminate the product transitive
  # dependency from export -> compile.
  task(name='c-for-ctypes', action=CCompile).install('native-compile')
  task(name='cpp-for-ctypes', action=CppCompile).install('native-compile')
  task(name='shared-libraries', action=LinkSharedLibraries).install('link')


def rules():
  return (
    create_native_environment_rules() +
    create_native_toolchain_rules() +
    create_xcode_cli_tools_rules() +
    create_binutils_rules() +
    create_gcc_rules() +
    create_llvm_rules()
  )
