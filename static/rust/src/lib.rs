pub mod commands;
pub mod protocol;
pub mod types;

pub use types::*;

#[typetag::serde(tag = "type")]
pub trait Command: 'static  {
}
