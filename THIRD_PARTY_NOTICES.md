# Third-Party Notices

This document acknowledges the third-party data sources and libraries used in the **english-lean** project.

---

## Data Sources

The following public vocabulary databases are planned for use in this project. Each entry is linked to its original repository where license details can be found.

### ECDICT
- **Repository**: https://github.com/skywind3000/ECDICT
- **License**: MIT License
- **Description**: Large-scale English-Chinese dictionary database with frequency data, definitions, and word levels.
- **Usage**: Source for CET-4 and graduate entrance exam (考研) vocabulary.

### CET4-6 Vocabulary (lyandut)
- **Repository**: https://github.com/lyandut/CET4-6
- **License**: MIT License
- **Description**: Organized vocabulary lists for CET-4, CET-6, and graduate entrance exams.
- **Usage**: Supplementary source for exam-specific vocabulary.

### Exam Vocabulary (issiki)
- **Repository**: https://github.com/issiki/english-word-lists
- **License**: MIT License
- **Description**: English word lists for various exams including CET-4, CET-6, and graduate entrance exams.
- **Usage**: Reference for exam vocabulary organization.

---

## Python Dependencies

This project uses the following Python packages. License information can be found on PyPI or the respective project repositories.

| Package | License | Repository |
|---------|---------|------------|
| PySide6 | LGPL-3.0 | https://code.qt.io/cgit/pyside/pyside-setup.git |
| platformdirs | MIT | https://github.com/tox-dev/platformdirs |
| pytest | MIT | https://github.com/pytest-dev/pytest |
| ruff | MIT | https://github.com/astral-sh/ruff |

---

## Notes

1. **No full license texts are included in this file.** Full license texts can be found at the linked repositories above.

2. **Data usage:** When using vocabulary data from external sources, this project:
   - Transforms original data into a different JSON format
   - Does not redistribute the original data files
   - Users are expected to download source data separately if needed

3. **License compliance:** Before redistributing this project or using it commercially, verify that all data sources used are compatible with your intended use case.

---

*Last updated: 2026-04-10*
