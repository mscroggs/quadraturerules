"""Build library."""

import argparse
import os
import sys

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(os.path.join(path, ".."), "website"))
from quadraturerules_website import settings  # noqa: E402
from quadraturerules_website.rules import load_rule  # noqa: E402

parser = argparse.ArgumentParser(description="Build quadraturerules library")
parser.add_argument('library', metavar='library', nargs=1,
                    default=None, help="Library to build")

args = parser.parse_args()
lib = args.library[0]

assert lib in os.listdir(path)

source_dir = os.path.join(path, lib)
assert os.path.isdir(source_dir)
target_dir = os.path.join(path, f"{lib}.build")
if os.path.isdir(target_dir):
    os.system(f"rm -r {target_dir}")

os.mkdir(target_dir)

with open(os.path.join(os.path.join(path, ".."), "VERSION")) as f:
    version = f.read().strip()
with open(os.path.join(os.path.join(path, ".."), "LICENSE")) as f:
    license = "\n".join(f.read().split("\n")[2:])
with open(os.path.join(os.path.join(path, ".."), "README.md")) as f:
    readme = f.read()

rules = []
for file in os.listdir(settings.rules_path):
    if file.endswith(".qr"):
        rules.append(load_rule(file[:-3]))
rules.sort(key=lambda r: r.name())

domains = list(set(i.domain for r in rules for i in r.rules))


def replace(content, subs):
    """Replace templated code."""
    for a, b in subs:
        content = content.replace(f"{{{{{a}}}}}", b)
    parts = content.split("{{if ")
    content = parts[0]
    for p in parts[1:]:
        inner, rest = p.split("}}", 1)
        for a, b in subs:
            inner = inner.replace(a, b)
        content += f"{{{{if {inner}}}}}"
        content += rest
    return content


def family_replace(content, variable, family):
    """Replace templated code for a rule family."""
    return replace(content, [
        [f"{variable}.code", f"{family.code}"],
        [f"{variable}.index", f"{family.index}"],
        [f"{variable}.itype", family.itype],
        [f"{variable}.name", family.name()],
        [f"{variable}.PascalCaseName", family.name("PascalCase")],
        [f"{variable}.camelCaseName", family.name("camelCase")],
        [f"{variable}.snake_case_name", family.name("snake_case")],
    ])


def rule_replace(content, variable, rule):
    """Replace templated code for a rule."""
    return replace(content, [
        [f"{variable}.order", f"{rule.order}"],
        [f"{variable}.domain", rule.domain],
        [f"{variable}.points_as_list", "[" + ", ".join(
            ["[" + ", ".join([f"{c}" for c in p]) + "]" for p in rule.points]) + "]"],
        [f"{variable}.points_as_flat_list", "[" + ", ".join([
            f"{c}" for p in rule.points for c in p]) + "]"],
        [f"{variable}.weights_as_list", "[" + ", ".join([f"{w}" for w in rule.weights]) + "]"],
    ])


def domain_replace(content, variable, domain):
    """Replace templated code for a domain."""
    return replace(content, [
        [f"{variable}.index", f"{domains.index(domain)}"],
        [f"{variable}.PascalCaseName", domain[0].upper() + domain[1:].lower()],
        [f"{variable}.camelCaseName", domain.lower()],
        [f"{variable}.snake_case_name", domain.lower()],
        [f"{variable}.name", domain],
    ])


def is_true(condition):
    """Check if a condition is true."""
    a, op, b = condition.split(" ")
    match op:
        case "==":
            return a == b
        case "!=":
            return a != b
        case _:
            raise ValueError(f"Unsupported operator: {op}")


def sub(content, vars={}):
    """Make substitutions in a file."""
    content = content.replace("{{VERSION}}", version)
    content = content.replace("{{LICENSE}}", license)
    content = content.replace("{{README}}", readme)
    while "{{end for}}" in content:
        temp, after = content.split("{{end for}}", 1)
        if after.startswith("\n"):
            after = after[1:]
        while temp.endswith(" "):
            temp = temp[:-1]
        temp2 = temp.split("{{for ")
        before = "{{for ".join(temp2[:-1])
        var, inside = temp2[-1].split(" ", 1)
        while before.endswith(" "):
            before = before[:-1]
        content = before
        loop_over, inside = inside.split("}}", 1)
        if inside.startswith("\n"):
            inside = inside[1:]
        for v, value in vars.items():
            if loop_over == f"in {v}.rules":
                for rule in value.rules:
                    content += rule_replace(inside, var, rule)
                break
        else:
            match loop_over:
                case "in rules":
                    for rule in rules:
                        content += family_replace(inside, var, rule)
                case "in domains":
                    for domain in domains:
                        content += domain_replace(inside, var, domain)
                case _:
                    raise ValueError(f"Unsupported loop: {loop_over}")
        content += after
    while "{{end if}}" in content:
        temp, after = content.split("{{end if}}", 1)
        if after.startswith("\n"):
            after = after[1:]
        while temp.endswith(" "):
            temp = temp[:-1]
        temp2 = temp.split("{{if ")
        before = "{{if ".join(temp2[:-1])
        while before.endswith(" "):
            before = before[:-1]
        content = before
        condition, inside = temp2[-1].split("}}", 1)
        if inside.startswith("\n"):
            inside = inside[1:]
        if is_true(condition):
            content += inside
        content += after
    return content


def sub_and_copy_files(folder):
    """Make substitutions and copy all files recursively in a directory."""
    for file_ in os.listdir(os.path.join(source_dir, folder)):
        file = os.path.join(folder, file_)
        if file_.startswith("."):
            continue
        if os.path.isdir(os.path.join(source_dir, file)):
            os.mkdir(os.path.join(target_dir, file))
            sub_and_copy_files(file)
        elif file.endswith(".template"):
            with open(os.path.join(source_dir, file)) as f:
                content = f.read()
            _, metadata_, content = content.split("--\n", 2)
            metadata = {}
            for line in metadata_.strip().split("\n"):
                var, value = line.split(":", 1)
                metadata[var.strip()] = value.strip()
            var, loop_over = metadata["template"].split(" ", 1)
            match loop_over:
                case "in rule":
                    for rule in rules:
                        with open(os.path.join(
                            os.path.join(target_dir, folder),
                            family_replace(metadata["filename"], var, rule),
                        ), "w") as f:
                            f.write(sub(family_replace(content, var, rule), {var: rule}))
                case _:
                    raise ValueError(f"Unsupported loop: {loop_over}")
        else:
            with open(os.path.join(source_dir, file)) as f:
                content = f.read()
            with open(os.path.join(target_dir, file), "w") as f:
                f.write(sub(content))


sub_and_copy_files("")

# Linting
if lib == "python":
    os.system(f"cd {target_dir} && ruff format .")
if lib == "rust":
    os.system(f"cd {target_dir} && cargo fmt")
