use ast_grep_dynamic::{DynamicLang, Registration};
use serde::{Deserialize, Serialize};

use crate::utils::ErrorContext as EC;
use anyhow::{Context, Result};
use std::collections::HashMap;
use std::path::{Path, PathBuf};

#[derive(Serialize, Deserialize, Clone)]
#[serde(rename_all = "camelCase")]
pub struct CustomLang {
  library_path: PathBuf,
  /// the dylib symbol to load ts-language, default is `tree_sitter_{name}`
  language_symbol: Option<String>,
  meta_var_char: Option<char>,
  expando_char: Option<char>,
  extensions: Vec<String>,
}

impl CustomLang {
  pub fn register(base: &Path, langs: HashMap<String, CustomLang>) -> Result<()> {
    let registrations = langs
      .into_iter()
      .map(|(name, custom)| to_registration(name, custom, base))
      .collect();
    let ret = unsafe { DynamicLang::register(registrations) };
    ret.context(EC::CustomLanguage)
  }
}

fn to_registration(name: String, custom_lang: CustomLang, base: &Path) -> Registration {
  let path = base.join(custom_lang.library_path);
  let sym = custom_lang
    .language_symbol
    .unwrap_or_else(|| format!("tree_sitter_{name}"));
  Registration {
    lang_name: name,
    lib_path: path,
    symbol: sym,
    meta_var_char: custom_lang.meta_var_char,
    expando_char: custom_lang.expando_char,
    extensions: custom_lang.extensions,
  }
}

#[cfg(test)]
mod test {
  use super::*;
  use serde_yaml::from_str;

  #[test]
  fn test_custom_lang() {
    let yaml = r"
libraryPath: a/b/c.so
extensions: [d, e, f]";
    let cus: CustomLang = from_str(yaml).unwrap();
    assert_eq!(cus.language_symbol, None);
    assert_eq!(cus.extensions, vec!["d", "e", "f"]);
  }
}
