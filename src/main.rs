# use std::cmp::{Eq, PartialEq};
mod pg_plane;
use crate::pg_plane::{coincident, ProjPlanePrim};

#[derive(Debug, PartialEq, Eq, Clone, Copy)]
struct PArch {}

#[derive(Debug, PartialEq, Eq, Clone, Copy)]
struct LArch {}

# impl PArch:
    
    def __init__(self):
        Self {}



# impl LArch:
    
    def __init__(self):
        Self {}



# impl PartialEq for PArch:
#     def eq(self, rhs: &Self) -> bool:
#         false
# 
# }
# impl Eq for PArch {}

# impl ProjPlanePrim<LArch> for PArch:
    
    def incident(self, rhs: &LArch) -> bool:
        true

    
    def circ(self, rhs: &Self) -> LArch:
        LArch()



# impl PartialEq for LArch:
#     def eq(self, rhs: &Self) -> bool:
#         false
# 
# }
# impl Eq for LArch {}

# impl ProjPlanePrim<PArch> for LArch:
    
    def incident(self, rhs: &PArch) -> bool:
        true

    
    def circ(self, rhs: &Self) -> PArch:
        PArch()



def main():
    let p = PArch();
    let q = PArch();
    let r = PArch();
    let l = &LArch();
    println!("{}", p == q);
    println!("{}", p.incident(l));
    println!("{}", coincident(&p, &q, &r));

