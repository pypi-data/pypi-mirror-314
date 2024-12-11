## -*- mode: conf-toml; -*-

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"


[project]
name = "${pypi_name}"
version = "0.1.0"
description = "${description}"
readme = "README.md"
authors = [{name = "Your Name", email = "you@example.com"}]
keywords = ["${name}"]
classifiers = [
        % for classifier in sorted(classifiers):
        "${classifier}",
        % endfor

        # TODO: remove this if you intend to publish your project
        # (it's here by default, to prevent accidental publishing)
        "Private :: Do Not Upload",
]
# requires-python = ">= 3.9"
dependencies = [
        % for pkg, spec in requires.items():
        % if spec:
        "${pkg if spec is True else spec}",
        % endif
        % endfor

        # TODO: these may be needed to build/release package
        #'build',
        #'invoke',
        #'twine',
]


% if has_cli:
[project.scripts]
${pkg_name} = "${pkg_name}.commands:${pkg_name}_typer"
% endif


% for key, values in entry_points.items():
[project.entry-points."${key}"]
% for value in values:
<% parts = value.split(' = ') %>
"${parts[0]}" = "${parts[1]}"
% endfor
% endfor


# [project.urls]
# Homepage = "https://example.com/"
# Repository = "https://github.com/example/${pkg_name}"
# Issues = "https://github.com/example/${pkg_name}/issues"
# Changelog = "https://github.com/example/${pkg_name}/blob/master/CHANGELOG.md"


# [tool.commitizen]
# version_provider = "pep621"
# tag_format = "v$version"
# update_changelog_on_bump = true


[tool.hatch.build.targets.wheel]
packages = ["${pkg_name}"]
