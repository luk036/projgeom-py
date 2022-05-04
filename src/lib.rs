mod ck_plane;
# mod hyperbolic;
# mod elliptic;
mod pg_object;
mod pg_plane;
mod hyp_object;

use crate::ck_plane::*;
use crate::pg_plane::*;

#[cfg(test)]
mod tests:
    use crate::pg_plane::ProjPlanePrim;
    use crate::pg_plane::{check_axiom, coincident};

    #[derive(Debug, PartialEq, Eq, Clone, Copy)]
    struct PArch {}

    #[derive(Debug, PartialEq, Eq, Clone, Copy)]
    struct LArch {}

    impl PArch:
        
        def __init__(self):
            Self {}
    


    impl LArch:
        
        def __init__(self):
            Self {}
    


    impl ProjPlanePrim<LArch> for PArch:
        
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

    impl ProjPlanePrim<PArch> for LArch:
        
        def incident(self, rhs: &PArch) -> bool:
            true
    
        
        def circ(self, rhs: &Self) -> PArch:
            PArch()
    


    #[test]
    def it_works():
        let p = PArch();
        let q = PArch();
        let r = PArch();
        let l = &LArch();
        println!("{}", p == q);
        println!("{}", p.incident(l));
        println!("{}", coincident(&p, &q, &r));
        check_axiom(&p, &q, &l);


