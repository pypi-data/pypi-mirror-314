# chemelem
Chemical elements with atomic masses and radii

This package implements getting atomic masses or covalent radii
by element or atomic number. It is simpler and loads faster than
much more advanced alternatives, such as
[mendeleev](https://pypi.org/project/mendeleev/).

## Usage
The package provides dict-like objects: `mass`, `covalent_radius`, 
and `chemelem`, which can be indexed by atomic number 
(`int`, from 1 to 118) or element symbol (`str` such as `'Cl'`).

* Getting the atomic mass (standard, isotope-weighted atomic weight) in amu:
  ```python
  import chemelem as ce
  ce.mass['Cl']
  ce.mass[17]
  ```  
  Both give the same result: `35.47`

* Getting the covalent radius (value in pm):
  ```python
  import chemelem as ce
  ce.covalent_radius['Fe']
  ce.covalent_radius[26]
  ```
  Both give the same result: `116.0`.

* Getting all the element's properties as dictionary:
  ```python
  import chemelem as ce
  ce.chemelem['Cl']
  ce.chemelem[17]
  ```
  Both give the same result: 
  `{'atomic_number': 'Cl', 'symbol': 'Cl', 'mass': 35.45, 'covalent_radius': 99.0}`.

* The elements properties can be also obtained using the `chemelem` console script
  ```bash
  chemelem Cl
  ```
