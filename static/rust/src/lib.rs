pub mod commands;
pub mod protocol;
pub mod types;

pub use types::*;

#[typetag::serde(tag = "type")]
pub trait Command: 'static {
	fn as_any(&self) -> &dyn std::any::Any;
}

#[typetag::serde(tag = "type")]
pub trait TxnResult: 'static  {
	fn as_any(&self) -> &dyn std::any::Any;
}
