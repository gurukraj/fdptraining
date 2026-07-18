"""
Consolidation script: merges all five part-PPTX files into a single final deck.

Each part was generated independently using the shared slide_helpers module.
This script creates a fresh presentation and calls each part's build() function
in order so that slides are numbered sequentially.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from slide_helpers import new_presentation, save_deck

# Import each part's build function
from part1_opening import build as build_part1
from part2_tools_spec import build as build_part2
from part3_arch_codegen import build as build_part3
from part4_test_sec_cicd import build as build_part4
from part5_agent_gov_close import build as build_part5

def main():
    print("=== Consolidating AI-Native Software Development Deck ===")
    prs = new_presentation()

    print("  Building Part 1: Opening (slides 1-6)...")
    n = build_part1(prs, start_num=1)
    print(f"    -> finished at slide {n - 1}")

    print("  Building Part 2: Tools & Spec-Driven (slides 7-13)...")
    n = build_part2(prs, start_num=n)
    print(f"    -> finished at slide {n - 1}")

    print("  Building Part 3: Architecture & Code Gen (slides 14-22)...")
    n = build_part3(prs, start_num=n)
    print(f"    -> finished at slide {n - 1}")

    print("  Building Part 4: Testing, Security, CI/CD (slides 23-32)...")
    n = build_part4(prs, start_num=n)
    print(f"    -> finished at slide {n - 1}")

    print("  Building Part 5: Multi-Agent, Governance, Closing, Backup (slides 33-50)...")
    n = build_part5(prs, start_num=n)
    print(f"    -> finished at slide {n - 1}")

    total = n - 1
    print(f"\n  Total slides: {total}")

    out = save_deck(prs, "AI_Native_Software_Development_Final.pptx")
    print(f"\n=== DONE: {out} ===")

if __name__ == "__main__":
    main()
