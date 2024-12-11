
// Generated from D:/a/pyA2L/pyA2L/pya2l/aml.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"
#include "amlVisitor.h"


/**
 * This class provides an empty implementation of amlVisitor, which can be
 * extended to create a visitor which only needs to handle a subset of the available methods.
 */
class  amlBaseVisitor : public amlVisitor {
public:

  virtual std::any visitAmlFile(amlParser::AmlFileContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitDeclaration(amlParser::DeclarationContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitType_definition(amlParser::Type_definitionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitType_name(amlParser::Type_nameContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitPredefined_type_name(amlParser::Predefined_type_nameContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitBlock_definition(amlParser::Block_definitionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitEnum_type_name(amlParser::Enum_type_nameContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitEnumerator_list(amlParser::Enumerator_listContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitEnumerator(amlParser::EnumeratorContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStruct_type_name(amlParser::Struct_type_nameContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStruct_member(amlParser::Struct_memberContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitMember(amlParser::MemberContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitArray_specifier(amlParser::Array_specifierContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTaggedstruct_type_name(amlParser::Taggedstruct_type_nameContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTaggedstruct_member(amlParser::Taggedstruct_memberContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTaggedstruct_definition(amlParser::Taggedstruct_definitionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTaggedunion_type_name(amlParser::Taggedunion_type_nameContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTagged_union_member(amlParser::Tagged_union_memberContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitNumericValue(amlParser::NumericValueContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStringValue(amlParser::StringValueContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTagValue(amlParser::TagValueContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitIdentifierValue(amlParser::IdentifierValueContext *ctx) override {
    return visitChildren(ctx);
  }


};

