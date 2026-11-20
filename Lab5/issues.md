# Static Analysis Issues

| Issue | Severity | Type | Line(s) | Description | Fix Approach |
|-------|----------|------|---------|-------------|--------------|
| Flask debug mode enabled | High | Security / Bandit B201 | 156 | `app.run(debug=True)` exposes the Werkzeug debugger and could permit code execution. | Run the Flask app with `debug=False`. |
| Remote logging listener enabled | Medium | Security / Bandit B612 | 136-139 | `logging.config.listen(9999)` opens a network listener and creates an unsafe remote configuration surface. | Disable remote logging in the demo and return an explicit disabled status. |
| Unsafe YAML loading | High | Security | 28 | `yaml.Loader` can construct unsafe Python objects from YAML input. | Replace it with `yaml.safe_load`. |
| Hard-coded Warden credential | High | Security | 64-70 (original) | The original database helper embedded a real-looking password and credential arguments. | Remove credential material and use a credential-free mock connection result. |
| Room capacity overflow | High | Logic | 42-73 | The original check used `len(...) > capacity`, allowing the room to reach one bed over capacity. | Check `>=` before allocating and reject full rooms. |
| Vacate did not remove occupants | High | Logic | 76-86 | `vacateRoom` deleted the allocation but left the student in the room's occupant list. | Remove the student from both state structures. |
| Gender ignored | Medium | Logic | 42-73 | The `gender` argument was unused, so male and female students could share unsuitable rooms. | Match the student's gender against the room block gender. |
| Vacant beds counted only empty rooms | Medium | Logic | 111-115 | Partially occupied rooms contributed zero rather than their remaining bed count. | Return capacity minus occupant count for every room. |
| Reallocation moved duplicate students | High | Logic | 42-73 | A duplicate ID was checked after the room loop, causing it to move to a potentially later room. | Vacate an existing allocation before searching for a compatible room. |
| Seniority order reversed | Medium | Logic | 101-104 | The original ascending sort put first-year students before final-year students despite the senior-first label. | Sort by year in descending order. |
| Mutable default argument | Medium | Pylint W0102 | 42 | `preferred=[]` could retain state across calls. | Use `preferred=None` and normalize it locally. |
| Invalid year handling | Medium | Logic / Pylint | 42-45 | Exact `type(year) != int` rejected subclasses and produced unclear behavior. | Use `isinstance(year, int)` and reject booleans. |
| Duplicate/invalid input handling | Medium | Logic | 42-73 | The original code could append duplicate IDs or reference missing preferred rooms. | Normalize candidates, skip missing rooms, and prevent duplicate waitlist entries. |
| Missing input escaping | Medium | Security | 143-151 | Concatenating request input and allocation data into HTML could enable injection. | Escape request input and allocation text before rendering. |
| Naming and style issues | Low | Pylint / Flake8 | File-wide | Unused imports, missing docstrings, camelCase names, and formatting violations reduced quality. | Add docstrings, remove unused imports, use snake_case, and format code consistently. |
