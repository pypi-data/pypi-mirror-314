mod error;
mod key;
mod value;

use std::ops::Deref;

pub use error::Error;
pub use key::{Key, KeyKind};
pub use value::{
    Array, ArrayKind, Boolean, Float, Integer, IntegerKind, LocalDate, LocalDateTime, LocalTime,
    OffsetDateTime, String, StringKind, Table, TableKind, Value,
};

#[derive(Debug, Clone, PartialEq)]
pub struct DocumentTree(Table);

impl From<DocumentTree> for Table {
    fn from(document: DocumentTree) -> Self {
        document.0
    }
}

impl Deref for DocumentTree {
    type Target = Table;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

enum RootItem {
    Table(Table),
    ArrayOfTables(Table),
    KeyValue(Table),
}

impl TryFrom<ast::Root> for DocumentTree {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::Root) -> Result<Self, Self::Error> {
        let mut document = Self(Table::new_root(&node));
        let mut errors = Vec::new();

        for item in node.items() {
            if let Err(errs) = match item.try_into() {
                Ok(
                    RootItem::Table(table)
                    | RootItem::ArrayOfTables(table)
                    | RootItem::KeyValue(table),
                ) => document.0.merge(table),
                Err(errs) => Err(errs),
            } {
                errors.extend(errs);
            }
        }

        if errors.is_empty() {
            Ok(document)
        } else {
            Err(errors)
        }
    }
}

impl TryFrom<ast::RootItem> for RootItem {
    type Error = Vec<crate::Error>;

    fn try_from(node: ast::RootItem) -> Result<Self, Self::Error> {
        match node {
            ast::RootItem::Table(table) => table.try_into().map(Self::Table),
            ast::RootItem::ArrayOfTables(array) => array.try_into().map(Self::ArrayOfTables),
            ast::RootItem::KeyValue(key_value) => key_value.try_into().map(Self::KeyValue),
        }
    }
}
