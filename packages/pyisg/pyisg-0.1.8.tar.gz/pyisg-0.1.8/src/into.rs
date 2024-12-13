use libisg::*;

use crate::*;

macro_rules! impl_from {
    ($type:tt) => {
        impl From<Wrapper<$type>> for $type {
            #[inline]
            fn from(value: Wrapper<$type>) -> $type {
                value.0
            }
        }
    };
}

impl_from!(Header);
impl_from!(Data);
impl_from!(ModelType);
impl_from!(DataType);
impl_from!(DataUnits);
impl_from!(DataFormat);
impl_from!(DataOrdering);
impl_from!(TideSystem);
impl_from!(CoordType);
impl_from!(CoordUnits);
impl_from!(CreationDate);
impl_from!(Coord);
