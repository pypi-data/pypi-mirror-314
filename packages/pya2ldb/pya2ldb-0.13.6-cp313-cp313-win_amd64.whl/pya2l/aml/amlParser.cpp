
// Generated from D:/a/pyA2L/pyA2L/pya2l/aml.g4 by ANTLR 4.13.2


#include "amlVisitor.h"

#include "amlParser.h"


using namespace antlrcpp;

using namespace antlr4;

namespace {

struct AmlParserStaticData final {
  AmlParserStaticData(std::vector<std::string> ruleNames,
                        std::vector<std::string> literalNames,
                        std::vector<std::string> symbolicNames)
      : ruleNames(std::move(ruleNames)), literalNames(std::move(literalNames)),
        symbolicNames(std::move(symbolicNames)),
        vocabulary(this->literalNames, this->symbolicNames) {}

  AmlParserStaticData(const AmlParserStaticData&) = delete;
  AmlParserStaticData(AmlParserStaticData&&) = delete;
  AmlParserStaticData& operator=(const AmlParserStaticData&) = delete;
  AmlParserStaticData& operator=(AmlParserStaticData&&) = delete;

  std::vector<antlr4::dfa::DFA> decisionToDFA;
  antlr4::atn::PredictionContextCache sharedContextCache;
  const std::vector<std::string> ruleNames;
  const std::vector<std::string> literalNames;
  const std::vector<std::string> symbolicNames;
  const antlr4::dfa::Vocabulary vocabulary;
  antlr4::atn::SerializedATNView serializedATN;
  std::unique_ptr<antlr4::atn::ATN> atn;
};

::antlr4::internal::OnceFlag amlParserOnceFlag;
#if ANTLR4_USE_THREAD_LOCAL_CACHE
static thread_local
#endif
std::unique_ptr<AmlParserStaticData> amlParserStaticData = nullptr;

void amlParserInitialize() {
#if ANTLR4_USE_THREAD_LOCAL_CACHE
  if (amlParserStaticData != nullptr) {
    return;
  }
#else
  assert(amlParserStaticData == nullptr);
#endif
  auto staticData = std::make_unique<AmlParserStaticData>(
    std::vector<std::string>{
      "amlFile", "declaration", "type_definition", "type_name", "predefined_type_name", 
      "block_definition", "enum_type_name", "enumerator_list", "enumerator", 
      "struct_type_name", "struct_member", "member", "array_specifier", 
      "taggedstruct_type_name", "taggedstruct_member", "taggedstruct_definition", 
      "taggedunion_type_name", "tagged_union_member", "numericValue", "stringValue", 
      "tagValue", "identifierValue"
    },
    std::vector<std::string>{
      "", "'/begin'", "'A2ML'", "'/end'", "';'", "'char'", "'int'", "'long'", 
      "'uchar'", "'uint'", "'ulong'", "'int64'", "'uint64'", "'double'", 
      "'float'", "'block'", "'enum'", "'{'", "'}'", "','", "'='", "'struct'", 
      "'['", "']'", "'taggedstruct'", "'('", "')'", "'*'", "'taggedunion'"
    },
    std::vector<std::string>{
      "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", 
      "", "", "", "", "", "", "", "", "", "", "", "", "INT", "HEX", "FLOAT", 
      "ID", "TAG", "COMMENT", "WS", "STRING"
    }
  );
  static const int32_t serializedATNSegment[] = {
  	4,1,36,253,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,6,2,
  	7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,2,14,7,
  	14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,7,20,2,21,7,
  	21,1,0,1,0,1,0,5,0,48,8,0,10,0,12,0,51,9,0,1,0,1,0,1,0,1,1,1,1,1,1,1,
  	1,1,1,1,1,3,1,62,8,1,1,2,1,2,1,3,1,3,1,3,1,3,1,3,3,3,71,8,3,1,4,1,4,1,
  	4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,3,4,83,8,4,1,5,1,5,1,5,1,5,1,6,1,6,3,6,
  	91,8,6,1,6,1,6,1,6,1,6,1,6,1,6,3,6,99,8,6,1,7,1,7,1,7,5,7,104,8,7,10,
  	7,12,7,107,9,7,1,8,1,8,1,8,3,8,112,8,8,1,9,1,9,3,9,116,8,9,1,9,1,9,5,
  	9,120,8,9,10,9,12,9,123,9,9,1,9,1,9,3,9,127,8,9,1,9,1,9,3,9,131,8,9,1,
  	10,1,10,3,10,135,8,10,1,11,1,11,5,11,139,8,11,10,11,12,11,142,9,11,1,
  	11,3,11,145,8,11,1,12,1,12,1,12,1,12,1,13,1,13,3,13,153,8,13,1,13,1,13,
  	5,13,157,8,13,10,13,12,13,160,9,13,1,13,1,13,3,13,164,8,13,1,13,1,13,
  	3,13,168,8,13,1,14,1,14,3,14,172,8,14,1,14,1,14,1,14,3,14,177,8,14,1,
  	14,1,14,1,14,1,14,1,14,1,14,3,14,185,8,14,1,14,1,14,1,14,3,14,190,8,14,
  	1,14,1,14,1,14,1,14,3,14,196,8,14,1,15,1,15,3,15,200,8,15,1,15,1,15,1,
  	15,1,15,3,15,206,8,15,1,15,1,15,1,15,3,15,211,8,15,1,16,1,16,3,16,215,
  	8,16,1,16,1,16,5,16,219,8,16,10,16,12,16,222,9,16,1,16,1,16,1,16,3,16,
  	227,8,16,1,17,1,17,3,17,231,8,17,1,17,3,17,234,8,17,1,17,1,17,3,17,238,
  	8,17,3,17,240,8,17,1,18,1,18,1,18,3,18,245,8,18,1,19,1,19,1,20,1,20,1,
  	21,1,21,1,21,0,0,22,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,
  	36,38,40,42,0,0,279,0,44,1,0,0,0,2,61,1,0,0,0,4,63,1,0,0,0,6,70,1,0,0,
  	0,8,82,1,0,0,0,10,84,1,0,0,0,12,98,1,0,0,0,14,100,1,0,0,0,16,108,1,0,
  	0,0,18,130,1,0,0,0,20,132,1,0,0,0,22,144,1,0,0,0,24,146,1,0,0,0,26,167,
  	1,0,0,0,28,195,1,0,0,0,30,210,1,0,0,0,32,226,1,0,0,0,34,239,1,0,0,0,36,
  	244,1,0,0,0,38,246,1,0,0,0,40,248,1,0,0,0,42,250,1,0,0,0,44,45,5,1,0,
  	0,45,49,5,2,0,0,46,48,3,2,1,0,47,46,1,0,0,0,48,51,1,0,0,0,49,47,1,0,0,
  	0,49,50,1,0,0,0,50,52,1,0,0,0,51,49,1,0,0,0,52,53,5,3,0,0,53,54,5,2,0,
  	0,54,1,1,0,0,0,55,56,3,4,2,0,56,57,5,4,0,0,57,62,1,0,0,0,58,59,3,10,5,
  	0,59,60,5,4,0,0,60,62,1,0,0,0,61,55,1,0,0,0,61,58,1,0,0,0,62,3,1,0,0,
  	0,63,64,3,6,3,0,64,5,1,0,0,0,65,71,3,8,4,0,66,71,3,18,9,0,67,71,3,26,
  	13,0,68,71,3,32,16,0,69,71,3,12,6,0,70,65,1,0,0,0,70,66,1,0,0,0,70,67,
  	1,0,0,0,70,68,1,0,0,0,70,69,1,0,0,0,71,7,1,0,0,0,72,83,5,5,0,0,73,83,
  	5,6,0,0,74,83,5,7,0,0,75,83,5,8,0,0,76,83,5,9,0,0,77,83,5,10,0,0,78,83,
  	5,11,0,0,79,83,5,12,0,0,80,83,5,13,0,0,81,83,5,14,0,0,82,72,1,0,0,0,82,
  	73,1,0,0,0,82,74,1,0,0,0,82,75,1,0,0,0,82,76,1,0,0,0,82,77,1,0,0,0,82,
  	78,1,0,0,0,82,79,1,0,0,0,82,80,1,0,0,0,82,81,1,0,0,0,83,9,1,0,0,0,84,
  	85,5,15,0,0,85,86,3,40,20,0,86,87,3,6,3,0,87,11,1,0,0,0,88,90,5,16,0,
  	0,89,91,3,42,21,0,90,89,1,0,0,0,90,91,1,0,0,0,91,92,1,0,0,0,92,93,5,17,
  	0,0,93,94,3,14,7,0,94,95,5,18,0,0,95,99,1,0,0,0,96,97,5,16,0,0,97,99,
  	3,42,21,0,98,88,1,0,0,0,98,96,1,0,0,0,99,13,1,0,0,0,100,105,3,16,8,0,
  	101,102,5,19,0,0,102,104,3,16,8,0,103,101,1,0,0,0,104,107,1,0,0,0,105,
  	103,1,0,0,0,105,106,1,0,0,0,106,15,1,0,0,0,107,105,1,0,0,0,108,111,3,
  	40,20,0,109,110,5,20,0,0,110,112,3,36,18,0,111,109,1,0,0,0,111,112,1,
  	0,0,0,112,17,1,0,0,0,113,115,5,21,0,0,114,116,3,42,21,0,115,114,1,0,0,
  	0,115,116,1,0,0,0,116,117,1,0,0,0,117,121,5,17,0,0,118,120,3,20,10,0,
  	119,118,1,0,0,0,120,123,1,0,0,0,121,119,1,0,0,0,121,122,1,0,0,0,122,124,
  	1,0,0,0,123,121,1,0,0,0,124,126,5,18,0,0,125,127,5,4,0,0,126,125,1,0,
  	0,0,126,127,1,0,0,0,127,131,1,0,0,0,128,129,5,21,0,0,129,131,3,42,21,
  	0,130,113,1,0,0,0,130,128,1,0,0,0,131,19,1,0,0,0,132,134,3,22,11,0,133,
  	135,5,4,0,0,134,133,1,0,0,0,134,135,1,0,0,0,135,21,1,0,0,0,136,140,3,
  	6,3,0,137,139,3,24,12,0,138,137,1,0,0,0,139,142,1,0,0,0,140,138,1,0,0,
  	0,140,141,1,0,0,0,141,145,1,0,0,0,142,140,1,0,0,0,143,145,3,10,5,0,144,
  	136,1,0,0,0,144,143,1,0,0,0,145,23,1,0,0,0,146,147,5,22,0,0,147,148,3,
  	36,18,0,148,149,5,23,0,0,149,25,1,0,0,0,150,152,5,24,0,0,151,153,3,42,
  	21,0,152,151,1,0,0,0,152,153,1,0,0,0,153,154,1,0,0,0,154,158,5,17,0,0,
  	155,157,3,28,14,0,156,155,1,0,0,0,157,160,1,0,0,0,158,156,1,0,0,0,158,
  	159,1,0,0,0,159,161,1,0,0,0,160,158,1,0,0,0,161,163,5,18,0,0,162,164,
  	5,4,0,0,163,162,1,0,0,0,163,164,1,0,0,0,164,168,1,0,0,0,165,166,5,24,
  	0,0,166,168,3,42,21,0,167,150,1,0,0,0,167,165,1,0,0,0,168,27,1,0,0,0,
  	169,171,3,30,15,0,170,172,5,4,0,0,171,170,1,0,0,0,171,172,1,0,0,0,172,
  	196,1,0,0,0,173,174,5,25,0,0,174,176,3,30,15,0,175,177,5,4,0,0,176,175,
  	1,0,0,0,176,177,1,0,0,0,177,178,1,0,0,0,178,179,5,26,0,0,179,180,5,27,
  	0,0,180,181,5,4,0,0,181,196,1,0,0,0,182,184,3,10,5,0,183,185,5,4,0,0,
  	184,183,1,0,0,0,184,185,1,0,0,0,185,196,1,0,0,0,186,187,5,25,0,0,187,
  	189,3,10,5,0,188,190,5,4,0,0,189,188,1,0,0,0,189,190,1,0,0,0,190,191,
  	1,0,0,0,191,192,5,26,0,0,192,193,5,27,0,0,193,194,5,4,0,0,194,196,1,0,
  	0,0,195,169,1,0,0,0,195,173,1,0,0,0,195,182,1,0,0,0,195,186,1,0,0,0,196,
  	29,1,0,0,0,197,199,3,40,20,0,198,200,3,22,11,0,199,198,1,0,0,0,199,200,
  	1,0,0,0,200,211,1,0,0,0,201,202,3,40,20,0,202,203,5,25,0,0,203,205,3,
  	22,11,0,204,206,5,4,0,0,205,204,1,0,0,0,205,206,1,0,0,0,206,207,1,0,0,
  	0,207,208,5,26,0,0,208,209,5,27,0,0,209,211,1,0,0,0,210,197,1,0,0,0,210,
  	201,1,0,0,0,211,31,1,0,0,0,212,214,5,28,0,0,213,215,3,42,21,0,214,213,
  	1,0,0,0,214,215,1,0,0,0,215,216,1,0,0,0,216,220,5,17,0,0,217,219,3,34,
  	17,0,218,217,1,0,0,0,219,222,1,0,0,0,220,218,1,0,0,0,220,221,1,0,0,0,
  	221,223,1,0,0,0,222,220,1,0,0,0,223,227,5,18,0,0,224,225,5,28,0,0,225,
  	227,3,42,21,0,226,212,1,0,0,0,226,224,1,0,0,0,227,33,1,0,0,0,228,230,
  	3,40,20,0,229,231,3,22,11,0,230,229,1,0,0,0,230,231,1,0,0,0,231,233,1,
  	0,0,0,232,234,5,4,0,0,233,232,1,0,0,0,233,234,1,0,0,0,234,240,1,0,0,0,
  	235,237,3,10,5,0,236,238,5,4,0,0,237,236,1,0,0,0,237,238,1,0,0,0,238,
  	240,1,0,0,0,239,228,1,0,0,0,239,235,1,0,0,0,240,35,1,0,0,0,241,245,5,
  	29,0,0,242,245,5,30,0,0,243,245,5,31,0,0,244,241,1,0,0,0,244,242,1,0,
  	0,0,244,243,1,0,0,0,245,37,1,0,0,0,246,247,5,36,0,0,247,39,1,0,0,0,248,
  	249,5,33,0,0,249,41,1,0,0,0,250,251,5,32,0,0,251,43,1,0,0,0,35,49,61,
  	70,82,90,98,105,111,115,121,126,130,134,140,144,152,158,163,167,171,176,
  	184,189,195,199,205,210,214,220,226,230,233,237,239,244
  };
  staticData->serializedATN = antlr4::atn::SerializedATNView(serializedATNSegment, sizeof(serializedATNSegment) / sizeof(serializedATNSegment[0]));

  antlr4::atn::ATNDeserializer deserializer;
  staticData->atn = deserializer.deserialize(staticData->serializedATN);

  const size_t count = staticData->atn->getNumberOfDecisions();
  staticData->decisionToDFA.reserve(count);
  for (size_t i = 0; i < count; i++) { 
    staticData->decisionToDFA.emplace_back(staticData->atn->getDecisionState(i), i);
  }
  amlParserStaticData = std::move(staticData);
}

}

amlParser::amlParser(TokenStream *input) : amlParser(input, antlr4::atn::ParserATNSimulatorOptions()) {}

amlParser::amlParser(TokenStream *input, const antlr4::atn::ParserATNSimulatorOptions &options) : Parser(input) {
  amlParser::initialize();
  _interpreter = new atn::ParserATNSimulator(this, *amlParserStaticData->atn, amlParserStaticData->decisionToDFA, amlParserStaticData->sharedContextCache, options);
}

amlParser::~amlParser() {
  delete _interpreter;
}

const atn::ATN& amlParser::getATN() const {
  return *amlParserStaticData->atn;
}

std::string amlParser::getGrammarFileName() const {
  return "aml.g4";
}

const std::vector<std::string>& amlParser::getRuleNames() const {
  return amlParserStaticData->ruleNames;
}

const dfa::Vocabulary& amlParser::getVocabulary() const {
  return amlParserStaticData->vocabulary;
}

antlr4::atn::SerializedATNView amlParser::getSerializedATN() const {
  return amlParserStaticData->serializedATN;
}


//----------------- AmlFileContext ------------------------------------------------------------------

amlParser::AmlFileContext::AmlFileContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<amlParser::DeclarationContext *> amlParser::AmlFileContext::declaration() {
  return getRuleContexts<amlParser::DeclarationContext>();
}

amlParser::DeclarationContext* amlParser::AmlFileContext::declaration(size_t i) {
  return getRuleContext<amlParser::DeclarationContext>(i);
}


size_t amlParser::AmlFileContext::getRuleIndex() const {
  return amlParser::RuleAmlFile;
}


std::any amlParser::AmlFileContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<amlVisitor*>(visitor))
    return parserVisitor->visitAmlFile(this);
  else
    return visitor->visitChildren(this);
}

amlParser::AmlFileContext* amlParser::amlFile() {
  AmlFileContext *_localctx = _tracker.createInstance<AmlFileContext>(_ctx, getState());
  enterRule(_localctx, 0, amlParser::RuleAmlFile);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(44);
    match(amlParser::T__0);
    setState(45);
    match(amlParser::T__1);
    setState(49);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & 287440864) != 0)) {
      setState(46);
      antlrcpp::downCast<AmlFileContext *>(_localctx)->declarationContext = declaration();
      antlrcpp::downCast<AmlFileContext *>(_localctx)->d.push_back(antlrcpp::downCast<AmlFileContext *>(_localctx)->declarationContext);
      setState(51);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(52);
    match(amlParser::T__2);
    setState(53);
    match(amlParser::T__1);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- DeclarationContext ------------------------------------------------------------------

amlParser::DeclarationContext::DeclarationContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

amlParser::Type_definitionContext* amlParser::DeclarationContext::type_definition() {
  return getRuleContext<amlParser::Type_definitionContext>(0);
}

amlParser::Block_definitionContext* amlParser::DeclarationContext::block_definition() {
  return getRuleContext<amlParser::Block_definitionContext>(0);
}


size_t amlParser::DeclarationContext::getRuleIndex() const {
  return amlParser::RuleDeclaration;
}


std::any amlParser::DeclarationContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<amlVisitor*>(visitor))
    return parserVisitor->visitDeclaration(this);
  else
    return visitor->visitChildren(this);
}

amlParser::DeclarationContext* amlParser::declaration() {
  DeclarationContext *_localctx = _tracker.createInstance<DeclarationContext>(_ctx, getState());
  enterRule(_localctx, 2, amlParser::RuleDeclaration);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(61);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case amlParser::T__4:
      case amlParser::T__5:
      case amlParser::T__6:
      case amlParser::T__7:
      case amlParser::T__8:
      case amlParser::T__9:
      case amlParser::T__10:
      case amlParser::T__11:
      case amlParser::T__12:
      case amlParser::T__13:
      case amlParser::T__15:
      case amlParser::T__20:
      case amlParser::T__23:
      case amlParser::T__27: {
        enterOuterAlt(_localctx, 1);
        setState(55);
        antlrcpp::downCast<DeclarationContext *>(_localctx)->t = type_definition();
        setState(56);
        match(amlParser::T__3);
        break;
      }

      case amlParser::T__14: {
        enterOuterAlt(_localctx, 2);
        setState(58);
        antlrcpp::downCast<DeclarationContext *>(_localctx)->b = block_definition();
        setState(59);
        match(amlParser::T__3);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Type_definitionContext ------------------------------------------------------------------

amlParser::Type_definitionContext::Type_definitionContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

amlParser::Type_nameContext* amlParser::Type_definitionContext::type_name() {
  return getRuleContext<amlParser::Type_nameContext>(0);
}


size_t amlParser::Type_definitionContext::getRuleIndex() const {
  return amlParser::RuleType_definition;
}


std::any amlParser::Type_definitionContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<amlVisitor*>(visitor))
    return parserVisitor->visitType_definition(this);
  else
    return visitor->visitChildren(this);
}

amlParser::Type_definitionContext* amlParser::type_definition() {
  Type_definitionContext *_localctx = _tracker.createInstance<Type_definitionContext>(_ctx, getState());
  enterRule(_localctx, 4, amlParser::RuleType_definition);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(63);
    type_name();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Type_nameContext ------------------------------------------------------------------

amlParser::Type_nameContext::Type_nameContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

amlParser::Predefined_type_nameContext* amlParser::Type_nameContext::predefined_type_name() {
  return getRuleContext<amlParser::Predefined_type_nameContext>(0);
}

amlParser::Struct_type_nameContext* amlParser::Type_nameContext::struct_type_name() {
  return getRuleContext<amlParser::Struct_type_nameContext>(0);
}

amlParser::Taggedstruct_type_nameContext* amlParser::Type_nameContext::taggedstruct_type_name() {
  return getRuleContext<amlParser::Taggedstruct_type_nameContext>(0);
}

amlParser::Taggedunion_type_nameContext* amlParser::Type_nameContext::taggedunion_type_name() {
  return getRuleContext<amlParser::Taggedunion_type_nameContext>(0);
}

amlParser::Enum_type_nameContext* amlParser::Type_nameContext::enum_type_name() {
  return getRuleContext<amlParser::Enum_type_nameContext>(0);
}


size_t amlParser::Type_nameContext::getRuleIndex() const {
  return amlParser::RuleType_name;
}


std::any amlParser::Type_nameContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<amlVisitor*>(visitor))
    return parserVisitor->visitType_name(this);
  else
    return visitor->visitChildren(this);
}

amlParser::Type_nameContext* amlParser::type_name() {
  Type_nameContext *_localctx = _tracker.createInstance<Type_nameContext>(_ctx, getState());
  enterRule(_localctx, 6, amlParser::RuleType_name);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(70);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case amlParser::T__4:
      case amlParser::T__5:
      case amlParser::T__6:
      case amlParser::T__7:
      case amlParser::T__8:
      case amlParser::T__9:
      case amlParser::T__10:
      case amlParser::T__11:
      case amlParser::T__12:
      case amlParser::T__13: {
        enterOuterAlt(_localctx, 1);
        setState(65);
        antlrcpp::downCast<Type_nameContext *>(_localctx)->pr = predefined_type_name();
        break;
      }

      case amlParser::T__20: {
        enterOuterAlt(_localctx, 2);
        setState(66);
        antlrcpp::downCast<Type_nameContext *>(_localctx)->st = struct_type_name();
        break;
      }

      case amlParser::T__23: {
        enterOuterAlt(_localctx, 3);
        setState(67);
        antlrcpp::downCast<Type_nameContext *>(_localctx)->ts = taggedstruct_type_name();
        break;
      }

      case amlParser::T__27: {
        enterOuterAlt(_localctx, 4);
        setState(68);
        antlrcpp::downCast<Type_nameContext *>(_localctx)->tu = taggedunion_type_name();
        break;
      }

      case amlParser::T__15: {
        enterOuterAlt(_localctx, 5);
        setState(69);
        antlrcpp::downCast<Type_nameContext *>(_localctx)->en = enum_type_name();
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Predefined_type_nameContext ------------------------------------------------------------------

amlParser::Predefined_type_nameContext::Predefined_type_nameContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t amlParser::Predefined_type_nameContext::getRuleIndex() const {
  return amlParser::RulePredefined_type_name;
}


std::any amlParser::Predefined_type_nameContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<amlVisitor*>(visitor))
    return parserVisitor->visitPredefined_type_name(this);
  else
    return visitor->visitChildren(this);
}

amlParser::Predefined_type_nameContext* amlParser::predefined_type_name() {
  Predefined_type_nameContext *_localctx = _tracker.createInstance<Predefined_type_nameContext>(_ctx, getState());
  enterRule(_localctx, 8, amlParser::RulePredefined_type_name);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(82);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case amlParser::T__4: {
        setState(72);
        antlrcpp::downCast<Predefined_type_nameContext *>(_localctx)->name = match(amlParser::T__4);
        break;
      }

      case amlParser::T__5: {
        setState(73);
        antlrcpp::downCast<Predefined_type_nameContext *>(_localctx)->name = match(amlParser::T__5);
        break;
      }

      case amlParser::T__6: {
        setState(74);
        antlrcpp::downCast<Predefined_type_nameContext *>(_localctx)->name = match(amlParser::T__6);
        break;
      }

      case amlParser::T__7: {
        setState(75);
        antlrcpp::downCast<Predefined_type_nameContext *>(_localctx)->name = match(amlParser::T__7);
        break;
      }

      case amlParser::T__8: {
        setState(76);
        antlrcpp::downCast<Predefined_type_nameContext *>(_localctx)->name = match(amlParser::T__8);
        break;
      }

      case amlParser::T__9: {
        setState(77);
        antlrcpp::downCast<Predefined_type_nameContext *>(_localctx)->name = match(amlParser::T__9);
        break;
      }

      case amlParser::T__10: {
        setState(78);
        antlrcpp::downCast<Predefined_type_nameContext *>(_localctx)->name = match(amlParser::T__10);
        break;
      }

      case amlParser::T__11: {
        setState(79);
        antlrcpp::downCast<Predefined_type_nameContext *>(_localctx)->name = match(amlParser::T__11);
        break;
      }

      case amlParser::T__12: {
        setState(80);
        antlrcpp::downCast<Predefined_type_nameContext *>(_localctx)->name = match(amlParser::T__12);
        break;
      }

      case amlParser::T__13: {
        setState(81);
        antlrcpp::downCast<Predefined_type_nameContext *>(_localctx)->name = match(amlParser::T__13);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Block_definitionContext ------------------------------------------------------------------

amlParser::Block_definitionContext::Block_definitionContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

amlParser::TagValueContext* amlParser::Block_definitionContext::tagValue() {
  return getRuleContext<amlParser::TagValueContext>(0);
}

amlParser::Type_nameContext* amlParser::Block_definitionContext::type_name() {
  return getRuleContext<amlParser::Type_nameContext>(0);
}


size_t amlParser::Block_definitionContext::getRuleIndex() const {
  return amlParser::RuleBlock_definition;
}


std::any amlParser::Block_definitionContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<amlVisitor*>(visitor))
    return parserVisitor->visitBlock_definition(this);
  else
    return visitor->visitChildren(this);
}

amlParser::Block_definitionContext* amlParser::block_definition() {
  Block_definitionContext *_localctx = _tracker.createInstance<Block_definitionContext>(_ctx, getState());
  enterRule(_localctx, 10, amlParser::RuleBlock_definition);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(84);
    match(amlParser::T__14);
    setState(85);
    antlrcpp::downCast<Block_definitionContext *>(_localctx)->tag = tagValue();

    setState(86);
    antlrcpp::downCast<Block_definitionContext *>(_localctx)->tn = type_name();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Enum_type_nameContext ------------------------------------------------------------------

amlParser::Enum_type_nameContext::Enum_type_nameContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

amlParser::Enumerator_listContext* amlParser::Enum_type_nameContext::enumerator_list() {
  return getRuleContext<amlParser::Enumerator_listContext>(0);
}

amlParser::IdentifierValueContext* amlParser::Enum_type_nameContext::identifierValue() {
  return getRuleContext<amlParser::IdentifierValueContext>(0);
}


size_t amlParser::Enum_type_nameContext::getRuleIndex() const {
  return amlParser::RuleEnum_type_name;
}


std::any amlParser::Enum_type_nameContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<amlVisitor*>(visitor))
    return parserVisitor->visitEnum_type_name(this);
  else
    return visitor->visitChildren(this);
}

amlParser::Enum_type_nameContext* amlParser::enum_type_name() {
  Enum_type_nameContext *_localctx = _tracker.createInstance<Enum_type_nameContext>(_ctx, getState());
  enterRule(_localctx, 12, amlParser::RuleEnum_type_name);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(98);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 5, _ctx)) {
    case 1: {
      enterOuterAlt(_localctx, 1);
      setState(88);
      match(amlParser::T__15);
      setState(90);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == amlParser::ID) {
        setState(89);
        antlrcpp::downCast<Enum_type_nameContext *>(_localctx)->t0 = identifierValue();
      }
      setState(92);
      match(amlParser::T__16);
      setState(93);
      antlrcpp::downCast<Enum_type_nameContext *>(_localctx)->l = enumerator_list();
      setState(94);
      match(amlParser::T__17);
      break;
    }

    case 2: {
      enterOuterAlt(_localctx, 2);
      setState(96);
      match(amlParser::T__15);
      setState(97);
      antlrcpp::downCast<Enum_type_nameContext *>(_localctx)->t1 = identifierValue();
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Enumerator_listContext ------------------------------------------------------------------

amlParser::Enumerator_listContext::Enumerator_listContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<amlParser::EnumeratorContext *> amlParser::Enumerator_listContext::enumerator() {
  return getRuleContexts<amlParser::EnumeratorContext>();
}

amlParser::EnumeratorContext* amlParser::Enumerator_listContext::enumerator(size_t i) {
  return getRuleContext<amlParser::EnumeratorContext>(i);
}


size_t amlParser::Enumerator_listContext::getRuleIndex() const {
  return amlParser::RuleEnumerator_list;
}


std::any amlParser::Enumerator_listContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<amlVisitor*>(visitor))
    return parserVisitor->visitEnumerator_list(this);
  else
    return visitor->visitChildren(this);
}

amlParser::Enumerator_listContext* amlParser::enumerator_list() {
  Enumerator_listContext *_localctx = _tracker.createInstance<Enumerator_listContext>(_ctx, getState());
  enterRule(_localctx, 14, amlParser::RuleEnumerator_list);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(100);
    antlrcpp::downCast<Enumerator_listContext *>(_localctx)->enumeratorContext = enumerator();
    antlrcpp::downCast<Enumerator_listContext *>(_localctx)->ids.push_back(antlrcpp::downCast<Enumerator_listContext *>(_localctx)->enumeratorContext);
    setState(105);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == amlParser::T__18) {
      setState(101);
      match(amlParser::T__18);
      setState(102);
      antlrcpp::downCast<Enumerator_listContext *>(_localctx)->enumeratorContext = enumerator();
      antlrcpp::downCast<Enumerator_listContext *>(_localctx)->ids.push_back(antlrcpp::downCast<Enumerator_listContext *>(_localctx)->enumeratorContext);
      setState(107);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- EnumeratorContext ------------------------------------------------------------------

amlParser::EnumeratorContext::EnumeratorContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

amlParser::TagValueContext* amlParser::EnumeratorContext::tagValue() {
  return getRuleContext<amlParser::TagValueContext>(0);
}

amlParser::NumericValueContext* amlParser::EnumeratorContext::numericValue() {
  return getRuleContext<amlParser::NumericValueContext>(0);
}


size_t amlParser::EnumeratorContext::getRuleIndex() const {
  return amlParser::RuleEnumerator;
}


std::any amlParser::EnumeratorContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<amlVisitor*>(visitor))
    return parserVisitor->visitEnumerator(this);
  else
    return visitor->visitChildren(this);
}

amlParser::EnumeratorContext* amlParser::enumerator() {
  EnumeratorContext *_localctx = _tracker.createInstance<EnumeratorContext>(_ctx, getState());
  enterRule(_localctx, 16, amlParser::RuleEnumerator);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(108);
    antlrcpp::downCast<EnumeratorContext *>(_localctx)->t = tagValue();
    setState(111);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == amlParser::T__19) {
      setState(109);
      match(amlParser::T__19);
      setState(110);
      antlrcpp::downCast<EnumeratorContext *>(_localctx)->c = numericValue();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Struct_type_nameContext ------------------------------------------------------------------

amlParser::Struct_type_nameContext::Struct_type_nameContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

amlParser::IdentifierValueContext* amlParser::Struct_type_nameContext::identifierValue() {
  return getRuleContext<amlParser::IdentifierValueContext>(0);
}

std::vector<amlParser::Struct_memberContext *> amlParser::Struct_type_nameContext::struct_member() {
  return getRuleContexts<amlParser::Struct_memberContext>();
}

amlParser::Struct_memberContext* amlParser::Struct_type_nameContext::struct_member(size_t i) {
  return getRuleContext<amlParser::Struct_memberContext>(i);
}


size_t amlParser::Struct_type_nameContext::getRuleIndex() const {
  return amlParser::RuleStruct_type_name;
}


std::any amlParser::Struct_type_nameContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<amlVisitor*>(visitor))
    return parserVisitor->visitStruct_type_name(this);
  else
    return visitor->visitChildren(this);
}

amlParser::Struct_type_nameContext* amlParser::struct_type_name() {
  Struct_type_nameContext *_localctx = _tracker.createInstance<Struct_type_nameContext>(_ctx, getState());
  enterRule(_localctx, 18, amlParser::RuleStruct_type_name);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(130);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 11, _ctx)) {
    case 1: {
      enterOuterAlt(_localctx, 1);
      setState(113);
      match(amlParser::T__20);
      setState(115);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == amlParser::ID) {
        setState(114);
        antlrcpp::downCast<Struct_type_nameContext *>(_localctx)->t0 = identifierValue();
      }
      setState(117);
      match(amlParser::T__16);
      setState(121);
      _errHandler->sync(this);
      _la = _input->LA(1);
      while ((((_la & ~ 0x3fULL) == 0) &&
        ((1ULL << _la) & 287440864) != 0)) {
        setState(118);
        antlrcpp::downCast<Struct_type_nameContext *>(_localctx)->struct_memberContext = struct_member();
        antlrcpp::downCast<Struct_type_nameContext *>(_localctx)->l.push_back(antlrcpp::downCast<Struct_type_nameContext *>(_localctx)->struct_memberContext);
        setState(123);
        _errHandler->sync(this);
        _la = _input->LA(1);
      }
      setState(124);
      match(amlParser::T__17);
      setState(126);
      _errHandler->sync(this);

      switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 10, _ctx)) {
      case 1: {
        setState(125);
        match(amlParser::T__3);
        break;
      }

      default:
        break;
      }
      break;
    }

    case 2: {
      enterOuterAlt(_localctx, 2);
      setState(128);
      match(amlParser::T__20);
      setState(129);
      antlrcpp::downCast<Struct_type_nameContext *>(_localctx)->t1 = identifierValue();
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Struct_memberContext ------------------------------------------------------------------

amlParser::Struct_memberContext::Struct_memberContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

amlParser::MemberContext* amlParser::Struct_memberContext::member() {
  return getRuleContext<amlParser::MemberContext>(0);
}


size_t amlParser::Struct_memberContext::getRuleIndex() const {
  return amlParser::RuleStruct_member;
}


std::any amlParser::Struct_memberContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<amlVisitor*>(visitor))
    return parserVisitor->visitStruct_member(this);
  else
    return visitor->visitChildren(this);
}

amlParser::Struct_memberContext* amlParser::struct_member() {
  Struct_memberContext *_localctx = _tracker.createInstance<Struct_memberContext>(_ctx, getState());
  enterRule(_localctx, 20, amlParser::RuleStruct_member);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(132);
    antlrcpp::downCast<Struct_memberContext *>(_localctx)->m = member();
    setState(134);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == amlParser::T__3) {
      setState(133);
      match(amlParser::T__3);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- MemberContext ------------------------------------------------------------------

amlParser::MemberContext::MemberContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

amlParser::Type_nameContext* amlParser::MemberContext::type_name() {
  return getRuleContext<amlParser::Type_nameContext>(0);
}

std::vector<amlParser::Array_specifierContext *> amlParser::MemberContext::array_specifier() {
  return getRuleContexts<amlParser::Array_specifierContext>();
}

amlParser::Array_specifierContext* amlParser::MemberContext::array_specifier(size_t i) {
  return getRuleContext<amlParser::Array_specifierContext>(i);
}

amlParser::Block_definitionContext* amlParser::MemberContext::block_definition() {
  return getRuleContext<amlParser::Block_definitionContext>(0);
}


size_t amlParser::MemberContext::getRuleIndex() const {
  return amlParser::RuleMember;
}


std::any amlParser::MemberContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<amlVisitor*>(visitor))
    return parserVisitor->visitMember(this);
  else
    return visitor->visitChildren(this);
}

amlParser::MemberContext* amlParser::member() {
  MemberContext *_localctx = _tracker.createInstance<MemberContext>(_ctx, getState());
  enterRule(_localctx, 22, amlParser::RuleMember);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(144);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case amlParser::T__4:
      case amlParser::T__5:
      case amlParser::T__6:
      case amlParser::T__7:
      case amlParser::T__8:
      case amlParser::T__9:
      case amlParser::T__10:
      case amlParser::T__11:
      case amlParser::T__12:
      case amlParser::T__13:
      case amlParser::T__15:
      case amlParser::T__20:
      case amlParser::T__23:
      case amlParser::T__27: {
        enterOuterAlt(_localctx, 1);
        setState(136);
        antlrcpp::downCast<MemberContext *>(_localctx)->t = type_name();
        setState(140);
        _errHandler->sync(this);
        _la = _input->LA(1);
        while (_la == amlParser::T__21) {
          setState(137);
          antlrcpp::downCast<MemberContext *>(_localctx)->array_specifierContext = array_specifier();
          antlrcpp::downCast<MemberContext *>(_localctx)->a.push_back(antlrcpp::downCast<MemberContext *>(_localctx)->array_specifierContext);
          setState(142);
          _errHandler->sync(this);
          _la = _input->LA(1);
        }
        break;
      }

      case amlParser::T__14: {
        enterOuterAlt(_localctx, 2);
        setState(143);
        antlrcpp::downCast<MemberContext *>(_localctx)->b = block_definition();
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Array_specifierContext ------------------------------------------------------------------

amlParser::Array_specifierContext::Array_specifierContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

amlParser::NumericValueContext* amlParser::Array_specifierContext::numericValue() {
  return getRuleContext<amlParser::NumericValueContext>(0);
}


size_t amlParser::Array_specifierContext::getRuleIndex() const {
  return amlParser::RuleArray_specifier;
}


std::any amlParser::Array_specifierContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<amlVisitor*>(visitor))
    return parserVisitor->visitArray_specifier(this);
  else
    return visitor->visitChildren(this);
}

amlParser::Array_specifierContext* amlParser::array_specifier() {
  Array_specifierContext *_localctx = _tracker.createInstance<Array_specifierContext>(_ctx, getState());
  enterRule(_localctx, 24, amlParser::RuleArray_specifier);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(146);
    match(amlParser::T__21);
    setState(147);
    antlrcpp::downCast<Array_specifierContext *>(_localctx)->c = numericValue();
    setState(148);
    match(amlParser::T__22);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Taggedstruct_type_nameContext ------------------------------------------------------------------

amlParser::Taggedstruct_type_nameContext::Taggedstruct_type_nameContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

amlParser::IdentifierValueContext* amlParser::Taggedstruct_type_nameContext::identifierValue() {
  return getRuleContext<amlParser::IdentifierValueContext>(0);
}

std::vector<amlParser::Taggedstruct_memberContext *> amlParser::Taggedstruct_type_nameContext::taggedstruct_member() {
  return getRuleContexts<amlParser::Taggedstruct_memberContext>();
}

amlParser::Taggedstruct_memberContext* amlParser::Taggedstruct_type_nameContext::taggedstruct_member(size_t i) {
  return getRuleContext<amlParser::Taggedstruct_memberContext>(i);
}


size_t amlParser::Taggedstruct_type_nameContext::getRuleIndex() const {
  return amlParser::RuleTaggedstruct_type_name;
}


std::any amlParser::Taggedstruct_type_nameContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<amlVisitor*>(visitor))
    return parserVisitor->visitTaggedstruct_type_name(this);
  else
    return visitor->visitChildren(this);
}

amlParser::Taggedstruct_type_nameContext* amlParser::taggedstruct_type_name() {
  Taggedstruct_type_nameContext *_localctx = _tracker.createInstance<Taggedstruct_type_nameContext>(_ctx, getState());
  enterRule(_localctx, 26, amlParser::RuleTaggedstruct_type_name);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(167);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 18, _ctx)) {
    case 1: {
      enterOuterAlt(_localctx, 1);
      setState(150);
      match(amlParser::T__23);
      setState(152);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == amlParser::ID) {
        setState(151);
        antlrcpp::downCast<Taggedstruct_type_nameContext *>(_localctx)->t0 = identifierValue();
      }
      setState(154);
      match(amlParser::T__16);
      setState(158);
      _errHandler->sync(this);
      _la = _input->LA(1);
      while ((((_la & ~ 0x3fULL) == 0) &&
        ((1ULL << _la) & 8623521792) != 0)) {
        setState(155);
        antlrcpp::downCast<Taggedstruct_type_nameContext *>(_localctx)->taggedstruct_memberContext = taggedstruct_member();
        antlrcpp::downCast<Taggedstruct_type_nameContext *>(_localctx)->l.push_back(antlrcpp::downCast<Taggedstruct_type_nameContext *>(_localctx)->taggedstruct_memberContext);
        setState(160);
        _errHandler->sync(this);
        _la = _input->LA(1);
      }
      setState(161);
      match(amlParser::T__17);
      setState(163);
      _errHandler->sync(this);

      switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 17, _ctx)) {
      case 1: {
        setState(162);
        match(amlParser::T__3);
        break;
      }

      default:
        break;
      }
      break;
    }

    case 2: {
      enterOuterAlt(_localctx, 2);
      setState(165);
      match(amlParser::T__23);
      setState(166);
      antlrcpp::downCast<Taggedstruct_type_nameContext *>(_localctx)->t1 = identifierValue();
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Taggedstruct_memberContext ------------------------------------------------------------------

amlParser::Taggedstruct_memberContext::Taggedstruct_memberContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

amlParser::Taggedstruct_definitionContext* amlParser::Taggedstruct_memberContext::taggedstruct_definition() {
  return getRuleContext<amlParser::Taggedstruct_definitionContext>(0);
}

amlParser::Block_definitionContext* amlParser::Taggedstruct_memberContext::block_definition() {
  return getRuleContext<amlParser::Block_definitionContext>(0);
}


size_t amlParser::Taggedstruct_memberContext::getRuleIndex() const {
  return amlParser::RuleTaggedstruct_member;
}


std::any amlParser::Taggedstruct_memberContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<amlVisitor*>(visitor))
    return parserVisitor->visitTaggedstruct_member(this);
  else
    return visitor->visitChildren(this);
}

amlParser::Taggedstruct_memberContext* amlParser::taggedstruct_member() {
  Taggedstruct_memberContext *_localctx = _tracker.createInstance<Taggedstruct_memberContext>(_ctx, getState());
  enterRule(_localctx, 28, amlParser::RuleTaggedstruct_member);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(195);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 23, _ctx)) {
    case 1: {
      enterOuterAlt(_localctx, 1);
      setState(169);
      antlrcpp::downCast<Taggedstruct_memberContext *>(_localctx)->ts1 = taggedstruct_definition();
      setState(171);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == amlParser::T__3) {
        setState(170);
        match(amlParser::T__3);
      }
      break;
    }

    case 2: {
      enterOuterAlt(_localctx, 2);
      setState(173);
      match(amlParser::T__24);
      setState(174);
      antlrcpp::downCast<Taggedstruct_memberContext *>(_localctx)->ts0 = taggedstruct_definition();
      setState(176);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == amlParser::T__3) {
        setState(175);
        match(amlParser::T__3);
      }
      setState(178);
      match(amlParser::T__25);
      setState(179);
      match(amlParser::T__26);
      setState(180);
      match(amlParser::T__3);
      break;
    }

    case 3: {
      enterOuterAlt(_localctx, 3);
      setState(182);
      antlrcpp::downCast<Taggedstruct_memberContext *>(_localctx)->bl1 = block_definition();
      setState(184);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == amlParser::T__3) {
        setState(183);
        match(amlParser::T__3);
      }
      break;
    }

    case 4: {
      enterOuterAlt(_localctx, 4);
      setState(186);
      match(amlParser::T__24);
      setState(187);
      antlrcpp::downCast<Taggedstruct_memberContext *>(_localctx)->bl0 = block_definition();
      setState(189);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == amlParser::T__3) {
        setState(188);
        match(amlParser::T__3);
      }
      setState(191);
      match(amlParser::T__25);
      setState(192);
      match(amlParser::T__26);
      setState(193);
      match(amlParser::T__3);
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Taggedstruct_definitionContext ------------------------------------------------------------------

amlParser::Taggedstruct_definitionContext::Taggedstruct_definitionContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

amlParser::TagValueContext* amlParser::Taggedstruct_definitionContext::tagValue() {
  return getRuleContext<amlParser::TagValueContext>(0);
}

amlParser::MemberContext* amlParser::Taggedstruct_definitionContext::member() {
  return getRuleContext<amlParser::MemberContext>(0);
}


size_t amlParser::Taggedstruct_definitionContext::getRuleIndex() const {
  return amlParser::RuleTaggedstruct_definition;
}


std::any amlParser::Taggedstruct_definitionContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<amlVisitor*>(visitor))
    return parserVisitor->visitTaggedstruct_definition(this);
  else
    return visitor->visitChildren(this);
}

amlParser::Taggedstruct_definitionContext* amlParser::taggedstruct_definition() {
  Taggedstruct_definitionContext *_localctx = _tracker.createInstance<Taggedstruct_definitionContext>(_ctx, getState());
  enterRule(_localctx, 30, amlParser::RuleTaggedstruct_definition);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(210);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 26, _ctx)) {
    case 1: {
      enterOuterAlt(_localctx, 1);
      setState(197);
      antlrcpp::downCast<Taggedstruct_definitionContext *>(_localctx)->tag = tagValue();
      setState(199);
      _errHandler->sync(this);

      switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 24, _ctx)) {
      case 1: {
        setState(198);
        antlrcpp::downCast<Taggedstruct_definitionContext *>(_localctx)->mem = member();
        break;
      }

      default:
        break;
      }
      break;
    }

    case 2: {
      enterOuterAlt(_localctx, 2);
      setState(201);
      antlrcpp::downCast<Taggedstruct_definitionContext *>(_localctx)->tag = tagValue();
      setState(202);
      match(amlParser::T__24);
      setState(203);
      antlrcpp::downCast<Taggedstruct_definitionContext *>(_localctx)->mem = member();
      setState(205);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == amlParser::T__3) {
        setState(204);
        match(amlParser::T__3);
      }
      setState(207);
      match(amlParser::T__25);
      setState(208);
      match(amlParser::T__26);
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Taggedunion_type_nameContext ------------------------------------------------------------------

amlParser::Taggedunion_type_nameContext::Taggedunion_type_nameContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

amlParser::IdentifierValueContext* amlParser::Taggedunion_type_nameContext::identifierValue() {
  return getRuleContext<amlParser::IdentifierValueContext>(0);
}

std::vector<amlParser::Tagged_union_memberContext *> amlParser::Taggedunion_type_nameContext::tagged_union_member() {
  return getRuleContexts<amlParser::Tagged_union_memberContext>();
}

amlParser::Tagged_union_memberContext* amlParser::Taggedunion_type_nameContext::tagged_union_member(size_t i) {
  return getRuleContext<amlParser::Tagged_union_memberContext>(i);
}


size_t amlParser::Taggedunion_type_nameContext::getRuleIndex() const {
  return amlParser::RuleTaggedunion_type_name;
}


std::any amlParser::Taggedunion_type_nameContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<amlVisitor*>(visitor))
    return parserVisitor->visitTaggedunion_type_name(this);
  else
    return visitor->visitChildren(this);
}

amlParser::Taggedunion_type_nameContext* amlParser::taggedunion_type_name() {
  Taggedunion_type_nameContext *_localctx = _tracker.createInstance<Taggedunion_type_nameContext>(_ctx, getState());
  enterRule(_localctx, 32, amlParser::RuleTaggedunion_type_name);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(226);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 29, _ctx)) {
    case 1: {
      enterOuterAlt(_localctx, 1);
      setState(212);
      match(amlParser::T__27);
      setState(214);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == amlParser::ID) {
        setState(213);
        antlrcpp::downCast<Taggedunion_type_nameContext *>(_localctx)->t0 = identifierValue();
      }
      setState(216);
      match(amlParser::T__16);
      setState(220);
      _errHandler->sync(this);
      _la = _input->LA(1);
      while (_la == amlParser::T__14

      || _la == amlParser::TAG) {
        setState(217);
        antlrcpp::downCast<Taggedunion_type_nameContext *>(_localctx)->tagged_union_memberContext = tagged_union_member();
        antlrcpp::downCast<Taggedunion_type_nameContext *>(_localctx)->l.push_back(antlrcpp::downCast<Taggedunion_type_nameContext *>(_localctx)->tagged_union_memberContext);
        setState(222);
        _errHandler->sync(this);
        _la = _input->LA(1);
      }
      setState(223);
      match(amlParser::T__17);
      break;
    }

    case 2: {
      enterOuterAlt(_localctx, 2);
      setState(224);
      match(amlParser::T__27);
      setState(225);
      antlrcpp::downCast<Taggedunion_type_nameContext *>(_localctx)->t1 = identifierValue();
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Tagged_union_memberContext ------------------------------------------------------------------

amlParser::Tagged_union_memberContext::Tagged_union_memberContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

amlParser::TagValueContext* amlParser::Tagged_union_memberContext::tagValue() {
  return getRuleContext<amlParser::TagValueContext>(0);
}

amlParser::MemberContext* amlParser::Tagged_union_memberContext::member() {
  return getRuleContext<amlParser::MemberContext>(0);
}

amlParser::Block_definitionContext* amlParser::Tagged_union_memberContext::block_definition() {
  return getRuleContext<amlParser::Block_definitionContext>(0);
}


size_t amlParser::Tagged_union_memberContext::getRuleIndex() const {
  return amlParser::RuleTagged_union_member;
}


std::any amlParser::Tagged_union_memberContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<amlVisitor*>(visitor))
    return parserVisitor->visitTagged_union_member(this);
  else
    return visitor->visitChildren(this);
}

amlParser::Tagged_union_memberContext* amlParser::tagged_union_member() {
  Tagged_union_memberContext *_localctx = _tracker.createInstance<Tagged_union_memberContext>(_ctx, getState());
  enterRule(_localctx, 34, amlParser::RuleTagged_union_member);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(239);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case amlParser::TAG: {
        enterOuterAlt(_localctx, 1);
        setState(228);
        antlrcpp::downCast<Tagged_union_memberContext *>(_localctx)->t = tagValue();
        setState(230);
        _errHandler->sync(this);

        switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 30, _ctx)) {
        case 1: {
          setState(229);
          antlrcpp::downCast<Tagged_union_memberContext *>(_localctx)->m = member();
          break;
        }

        default:
          break;
        }
        setState(233);
        _errHandler->sync(this);

        _la = _input->LA(1);
        if (_la == amlParser::T__3) {
          setState(232);
          match(amlParser::T__3);
        }
        break;
      }

      case amlParser::T__14: {
        enterOuterAlt(_localctx, 2);
        setState(235);
        antlrcpp::downCast<Tagged_union_memberContext *>(_localctx)->b = block_definition();
        setState(237);
        _errHandler->sync(this);

        _la = _input->LA(1);
        if (_la == amlParser::T__3) {
          setState(236);
          match(amlParser::T__3);
        }
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- NumericValueContext ------------------------------------------------------------------

amlParser::NumericValueContext::NumericValueContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* amlParser::NumericValueContext::INT() {
  return getToken(amlParser::INT, 0);
}

tree::TerminalNode* amlParser::NumericValueContext::HEX() {
  return getToken(amlParser::HEX, 0);
}

tree::TerminalNode* amlParser::NumericValueContext::FLOAT() {
  return getToken(amlParser::FLOAT, 0);
}


size_t amlParser::NumericValueContext::getRuleIndex() const {
  return amlParser::RuleNumericValue;
}


std::any amlParser::NumericValueContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<amlVisitor*>(visitor))
    return parserVisitor->visitNumericValue(this);
  else
    return visitor->visitChildren(this);
}

amlParser::NumericValueContext* amlParser::numericValue() {
  NumericValueContext *_localctx = _tracker.createInstance<NumericValueContext>(_ctx, getState());
  enterRule(_localctx, 36, amlParser::RuleNumericValue);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(244);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case amlParser::INT: {
        enterOuterAlt(_localctx, 1);
        setState(241);
        antlrcpp::downCast<NumericValueContext *>(_localctx)->i = match(amlParser::INT);
        break;
      }

      case amlParser::HEX: {
        enterOuterAlt(_localctx, 2);
        setState(242);
        antlrcpp::downCast<NumericValueContext *>(_localctx)->h = match(amlParser::HEX);
        break;
      }

      case amlParser::FLOAT: {
        enterOuterAlt(_localctx, 3);
        setState(243);
        antlrcpp::downCast<NumericValueContext *>(_localctx)->f = match(amlParser::FLOAT);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- StringValueContext ------------------------------------------------------------------

amlParser::StringValueContext::StringValueContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* amlParser::StringValueContext::STRING() {
  return getToken(amlParser::STRING, 0);
}


size_t amlParser::StringValueContext::getRuleIndex() const {
  return amlParser::RuleStringValue;
}


std::any amlParser::StringValueContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<amlVisitor*>(visitor))
    return parserVisitor->visitStringValue(this);
  else
    return visitor->visitChildren(this);
}

amlParser::StringValueContext* amlParser::stringValue() {
  StringValueContext *_localctx = _tracker.createInstance<StringValueContext>(_ctx, getState());
  enterRule(_localctx, 38, amlParser::RuleStringValue);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(246);
    antlrcpp::downCast<StringValueContext *>(_localctx)->s = match(amlParser::STRING);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- TagValueContext ------------------------------------------------------------------

amlParser::TagValueContext::TagValueContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* amlParser::TagValueContext::TAG() {
  return getToken(amlParser::TAG, 0);
}


size_t amlParser::TagValueContext::getRuleIndex() const {
  return amlParser::RuleTagValue;
}


std::any amlParser::TagValueContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<amlVisitor*>(visitor))
    return parserVisitor->visitTagValue(this);
  else
    return visitor->visitChildren(this);
}

amlParser::TagValueContext* amlParser::tagValue() {
  TagValueContext *_localctx = _tracker.createInstance<TagValueContext>(_ctx, getState());
  enterRule(_localctx, 40, amlParser::RuleTagValue);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(248);
    antlrcpp::downCast<TagValueContext *>(_localctx)->s = match(amlParser::TAG);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- IdentifierValueContext ------------------------------------------------------------------

amlParser::IdentifierValueContext::IdentifierValueContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* amlParser::IdentifierValueContext::ID() {
  return getToken(amlParser::ID, 0);
}


size_t amlParser::IdentifierValueContext::getRuleIndex() const {
  return amlParser::RuleIdentifierValue;
}


std::any amlParser::IdentifierValueContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<amlVisitor*>(visitor))
    return parserVisitor->visitIdentifierValue(this);
  else
    return visitor->visitChildren(this);
}

amlParser::IdentifierValueContext* amlParser::identifierValue() {
  IdentifierValueContext *_localctx = _tracker.createInstance<IdentifierValueContext>(_ctx, getState());
  enterRule(_localctx, 42, amlParser::RuleIdentifierValue);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(250);
    antlrcpp::downCast<IdentifierValueContext *>(_localctx)->i = match(amlParser::ID);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

void amlParser::initialize() {
#if ANTLR4_USE_THREAD_LOCAL_CACHE
  amlParserInitialize();
#else
  ::antlr4::internal::call_once(amlParserOnceFlag, amlParserInitialize);
#endif
}
