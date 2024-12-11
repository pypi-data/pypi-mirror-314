
// Generated from D:/a/pyA2L/pyA2L/pya2l/aml.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"
#include "amlParser.h"



/**
 * This class defines an abstract visitor for a parse tree
 * produced by amlParser.
 */
class  amlVisitor : public antlr4::tree::AbstractParseTreeVisitor {
public:

  /**
   * Visit parse trees produced by amlParser.
   */
    virtual std::any visitAmlFile(amlParser::AmlFileContext *context) = 0;

    virtual std::any visitDeclaration(amlParser::DeclarationContext *context) = 0;

    virtual std::any visitType_definition(amlParser::Type_definitionContext *context) = 0;

    virtual std::any visitType_name(amlParser::Type_nameContext *context) = 0;

    virtual std::any visitPredefined_type_name(amlParser::Predefined_type_nameContext *context) = 0;

    virtual std::any visitBlock_definition(amlParser::Block_definitionContext *context) = 0;

    virtual std::any visitEnum_type_name(amlParser::Enum_type_nameContext *context) = 0;

    virtual std::any visitEnumerator_list(amlParser::Enumerator_listContext *context) = 0;

    virtual std::any visitEnumerator(amlParser::EnumeratorContext *context) = 0;

    virtual std::any visitStruct_type_name(amlParser::Struct_type_nameContext *context) = 0;

    virtual std::any visitStruct_member(amlParser::Struct_memberContext *context) = 0;

    virtual std::any visitMember(amlParser::MemberContext *context) = 0;

    virtual std::any visitArray_specifier(amlParser::Array_specifierContext *context) = 0;

    virtual std::any visitTaggedstruct_type_name(amlParser::Taggedstruct_type_nameContext *context) = 0;

    virtual std::any visitTaggedstruct_member(amlParser::Taggedstruct_memberContext *context) = 0;

    virtual std::any visitTaggedstruct_definition(amlParser::Taggedstruct_definitionContext *context) = 0;

    virtual std::any visitTaggedunion_type_name(amlParser::Taggedunion_type_nameContext *context) = 0;

    virtual std::any visitTagged_union_member(amlParser::Tagged_union_memberContext *context) = 0;

    virtual std::any visitNumericValue(amlParser::NumericValueContext *context) = 0;

    virtual std::any visitStringValue(amlParser::StringValueContext *context) = 0;

    virtual std::any visitTagValue(amlParser::TagValueContext *context) = 0;

    virtual std::any visitIdentifierValue(amlParser::IdentifierValueContext *context) = 0;


};

