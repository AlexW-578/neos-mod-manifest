# API Schema

Top-level object:

- Schema version
- Content version? Maybe just use an etag for this.
- Mods map
  - Key: Mod GUID (reverse domain name notation preferred)
  - Value: Mod object
    - Name
    - Description
    - Author
    - Author URL
    - Source Location
    - Website
    - Tag list (list of strings) used for search?
    - Category (one string)
    - Flag list (list of strings) special meaning
    - Conflicts (list of mod GUIDs)
    - Dependencies map
      - Key: Dependency GUID
      - Value: Dependency map
        - Key: Mod GUID
        - Value: Dependency object
          - Version specifier
    - Version Map (this might be in a separate json object)
      - Key: Version number
      - Value: Version object
        - Changelog
        - ReleaseUrl
        - Neos version compatibility? (NOT semver `2022.1.28.1310` but `<` and `>` rules will work fine)
        - Modloader version compatibility? (semver)
        - Flag list (list of strings) special meaning, inherits from mod
        - Conflicts (list of mod GUIDs), inherits from mod
        - Mod dependencies? (circular dependencies are actually okay), list of mod GUIDs + version specifiers?. NML dependency is implied by default, inherits from mod
        - Artifact list
          - Artifact object
            - Download URL
            - File hash
            - Install location, defaults to `/nml_mods`

Flags:

- Mod Flags
  - `deprecated` Deprecated (maintainer is gone, users need to migrate)
  - `plugin` it needs a -LoadAssembly argument to work and it does not depend on NML
  - `file` it does not depend on NML
- Version Flags (mod flags are inherited)
  - Security Vulnerability
    - `vulnerablity:low` Low
    - `vulnerablity:medium` Medium
    - `vulnerablity:high` High
    - `vulnerablity:critical` Critical
  - `broken` Broken (different from incompatible, means the version itself is broken by design)
    - `broken:linux-native` Doesn't work on linux native
    - `broken:linux-wine` Doesn't work on linux wine/proton
    - `broken:windows` Doesn't work on windows
  - `prerelease` Mod dev wants to limit distribution
