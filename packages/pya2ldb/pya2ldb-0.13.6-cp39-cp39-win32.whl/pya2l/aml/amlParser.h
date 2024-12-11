
// Generated from D:/a/pyA2L/pyA2L/pya2l/aml.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"




class  amlParser : public antlr4::Parser {
public:
  enum {
    T__0 = 1, T__1 = 2, T__2 = 3, T__3 = 4, T__4 = 5, T__5 = 6, T__6 = 7, 
    T__7 = 8, T__8 = 9, T__9 = 10, T__10 = 11, T__11 = 12, T__12 = 13, T__13 = 14, 
    T__14 = 15, T__15 = 16, T__16 = 17, T__17 = 18, T__18 = 19, T__19 = 20, 
    T__20 = 21, T__21 = 22, T__22 = 23, T__23 = 24, T__24 = 25, T__25 = 26, 
    T__26 = 27, T__27 = 28, INT = 29, HEX = 30, FLOAT = 31, ID = 32, TAG = 33, 
    COMMENT = 34, WS = 35, STRING = 36
  };

  enum {
    RuleAmlFile = 0, RuleDeclaration = 1, RuleType_definition = 2, RuleType_name = 3, 
    RulePredefined_type_name = 4, RuleBlock_definition = 5, RuleEnum_type_name = 6, 
    RuleEnumerator_list = 7, RuleEnumerator = 8, RuleStruct_type_name = 9, 
    RuleStruct_member = 10, RuleMember = 11, RuleArray_specifier = 12, RuleTaggedstruct_type_name = 13, 
    RuleTaggedstruct_member = 14, RuleTaggedstruct_definition = 15, RuleTaggedunion_type_name = 16, 
    RuleTagged_union_member = 17, RuleNumericValue = 18, RuleStringValue = 19, 
    RuleTagValue = 20, RuleIdentifierValue = 21
  };

  explicit amlParser(antlr4::TokenStream *input);

  amlParser(antlr4::TokenStream *input, const antlr4::atn::ParserATNSimulatorOptions &options);

  ~amlParser() override;

  std::string getGrammarFileName() const override;

  const antlr4::atn::ATN& getATN() const override;

  const std::vector<std::string>& getRuleNames() const override;

  const antlr4::dfa::Vocabulary& getVocabulary() const override;

  antlr4::atn::SerializedATNView getSerializedATN() const override;


  class AmlFileContext;
  class DeclarationContext;
  class Type_definitionContext;
  class Type_nameContext;
  class Predefined_type_nameContext;
  class Block_definitionContext;
  class Enum_type_nameContext;
  class Enumerator_listContext;
  class EnumeratorContext;
  class Struct_type_nameContext;
  class Struct_memberContext;
  class MemberContext;
  class Array_specifierContext;
  class Taggedstruct_type_nameContext;
  class Taggedstruct_memberContext;
  class Taggedstruct_definitionContext;
  class Taggedunion_type_nameContext;
  class Tagged_union_memberContext;
  class NumericValueContext;
  class StringValueContext;
  class TagValueContext;
  class IdentifierValueContext; 

  class  AmlFileContext : public antlr4::ParserRuleContext {
  public:
    amlParser::DeclarationContext *declarationContext = nullptr;
    std::vector<DeclarationContext *> d;
    AmlFileContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<DeclarationContext *> declaration();
    DeclarationContext* declaration(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  AmlFileContext* amlFile();

  class  DeclarationContext : public antlr4::ParserRuleContext {
  public:
    amlParser::Type_definitionContext *t = nullptr;
    amlParser::Block_definitionContext *b = nullptr;
    DeclarationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Type_definitionContext *type_definition();
    Block_definitionContext *block_definition();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  DeclarationContext* declaration();

  class  Type_definitionContext : public antlr4::ParserRuleContext {
  public:
    Type_definitionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Type_nameContext *type_name();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Type_definitionContext* type_definition();

  class  Type_nameContext : public antlr4::ParserRuleContext {
  public:
    amlParser::Predefined_type_nameContext *pr = nullptr;
    amlParser::Struct_type_nameContext *st = nullptr;
    amlParser::Taggedstruct_type_nameContext *ts = nullptr;
    amlParser::Taggedunion_type_nameContext *tu = nullptr;
    amlParser::Enum_type_nameContext *en = nullptr;
    Type_nameContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Predefined_type_nameContext *predefined_type_name();
    Struct_type_nameContext *struct_type_name();
    Taggedstruct_type_nameContext *taggedstruct_type_name();
    Taggedunion_type_nameContext *taggedunion_type_name();
    Enum_type_nameContext *enum_type_name();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Type_nameContext* type_name();

  class  Predefined_type_nameContext : public antlr4::ParserRuleContext {
  public:
    antlr4::Token *name = nullptr;
    Predefined_type_nameContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Predefined_type_nameContext* predefined_type_name();

  class  Block_definitionContext : public antlr4::ParserRuleContext {
  public:
    amlParser::TagValueContext *tag = nullptr;
    amlParser::Type_nameContext *tn = nullptr;
    Block_definitionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    TagValueContext *tagValue();
    Type_nameContext *type_name();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Block_definitionContext* block_definition();

  class  Enum_type_nameContext : public antlr4::ParserRuleContext {
  public:
    amlParser::IdentifierValueContext *t0 = nullptr;
    amlParser::Enumerator_listContext *l = nullptr;
    amlParser::IdentifierValueContext *t1 = nullptr;
    Enum_type_nameContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Enumerator_listContext *enumerator_list();
    IdentifierValueContext *identifierValue();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Enum_type_nameContext* enum_type_name();

  class  Enumerator_listContext : public antlr4::ParserRuleContext {
  public:
    amlParser::EnumeratorContext *enumeratorContext = nullptr;
    std::vector<EnumeratorContext *> ids;
    Enumerator_listContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<EnumeratorContext *> enumerator();
    EnumeratorContext* enumerator(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Enumerator_listContext* enumerator_list();

  class  EnumeratorContext : public antlr4::ParserRuleContext {
  public:
    amlParser::TagValueContext *t = nullptr;
    amlParser::NumericValueContext *c = nullptr;
    EnumeratorContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    TagValueContext *tagValue();
    NumericValueContext *numericValue();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  EnumeratorContext* enumerator();

  class  Struct_type_nameContext : public antlr4::ParserRuleContext {
  public:
    amlParser::IdentifierValueContext *t0 = nullptr;
    amlParser::Struct_memberContext *struct_memberContext = nullptr;
    std::vector<Struct_memberContext *> l;
    amlParser::IdentifierValueContext *t1 = nullptr;
    Struct_type_nameContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierValueContext *identifierValue();
    std::vector<Struct_memberContext *> struct_member();
    Struct_memberContext* struct_member(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Struct_type_nameContext* struct_type_name();

  class  Struct_memberContext : public antlr4::ParserRuleContext {
  public:
    amlParser::MemberContext *m = nullptr;
    Struct_memberContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    MemberContext *member();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Struct_memberContext* struct_member();

  class  MemberContext : public antlr4::ParserRuleContext {
  public:
    amlParser::Type_nameContext *t = nullptr;
    amlParser::Array_specifierContext *array_specifierContext = nullptr;
    std::vector<Array_specifierContext *> a;
    amlParser::Block_definitionContext *b = nullptr;
    MemberContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Type_nameContext *type_name();
    std::vector<Array_specifierContext *> array_specifier();
    Array_specifierContext* array_specifier(size_t i);
    Block_definitionContext *block_definition();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  MemberContext* member();

  class  Array_specifierContext : public antlr4::ParserRuleContext {
  public:
    amlParser::NumericValueContext *c = nullptr;
    Array_specifierContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    NumericValueContext *numericValue();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Array_specifierContext* array_specifier();

  class  Taggedstruct_type_nameContext : public antlr4::ParserRuleContext {
  public:
    amlParser::IdentifierValueContext *t0 = nullptr;
    amlParser::Taggedstruct_memberContext *taggedstruct_memberContext = nullptr;
    std::vector<Taggedstruct_memberContext *> l;
    amlParser::IdentifierValueContext *t1 = nullptr;
    Taggedstruct_type_nameContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierValueContext *identifierValue();
    std::vector<Taggedstruct_memberContext *> taggedstruct_member();
    Taggedstruct_memberContext* taggedstruct_member(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Taggedstruct_type_nameContext* taggedstruct_type_name();

  class  Taggedstruct_memberContext : public antlr4::ParserRuleContext {
  public:
    amlParser::Taggedstruct_definitionContext *ts1 = nullptr;
    amlParser::Taggedstruct_definitionContext *ts0 = nullptr;
    amlParser::Block_definitionContext *bl1 = nullptr;
    amlParser::Block_definitionContext *bl0 = nullptr;
    Taggedstruct_memberContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Taggedstruct_definitionContext *taggedstruct_definition();
    Block_definitionContext *block_definition();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Taggedstruct_memberContext* taggedstruct_member();

  class  Taggedstruct_definitionContext : public antlr4::ParserRuleContext {
  public:
    amlParser::TagValueContext *tag = nullptr;
    amlParser::MemberContext *mem = nullptr;
    Taggedstruct_definitionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    TagValueContext *tagValue();
    MemberContext *member();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Taggedstruct_definitionContext* taggedstruct_definition();

  class  Taggedunion_type_nameContext : public antlr4::ParserRuleContext {
  public:
    amlParser::IdentifierValueContext *t0 = nullptr;
    amlParser::Tagged_union_memberContext *tagged_union_memberContext = nullptr;
    std::vector<Tagged_union_memberContext *> l;
    amlParser::IdentifierValueContext *t1 = nullptr;
    Taggedunion_type_nameContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierValueContext *identifierValue();
    std::vector<Tagged_union_memberContext *> tagged_union_member();
    Tagged_union_memberContext* tagged_union_member(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Taggedunion_type_nameContext* taggedunion_type_name();

  class  Tagged_union_memberContext : public antlr4::ParserRuleContext {
  public:
    amlParser::TagValueContext *t = nullptr;
    amlParser::MemberContext *m = nullptr;
    amlParser::Block_definitionContext *b = nullptr;
    Tagged_union_memberContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    TagValueContext *tagValue();
    MemberContext *member();
    Block_definitionContext *block_definition();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Tagged_union_memberContext* tagged_union_member();

  class  NumericValueContext : public antlr4::ParserRuleContext {
  public:
    antlr4::Token *i = nullptr;
    antlr4::Token *h = nullptr;
    antlr4::Token *f = nullptr;
    NumericValueContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *INT();
    antlr4::tree::TerminalNode *HEX();
    antlr4::tree::TerminalNode *FLOAT();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  NumericValueContext* numericValue();

  class  StringValueContext : public antlr4::ParserRuleContext {
  public:
    antlr4::Token *s = nullptr;
    StringValueContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *STRING();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  StringValueContext* stringValue();

  class  TagValueContext : public antlr4::ParserRuleContext {
  public:
    antlr4::Token *s = nullptr;
    TagValueContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *TAG();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  TagValueContext* tagValue();

  class  IdentifierValueContext : public antlr4::ParserRuleContext {
  public:
    antlr4::Token *i = nullptr;
    IdentifierValueContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *ID();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  IdentifierValueContext* identifierValue();


  // By default the static state used to implement the parser is lazily initialized during the first
  // call to the constructor. You can call this function if you wish to initialize the static state
  // ahead of time.
  static void initialize();

private:
};

