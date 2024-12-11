
// Generated from D:/a/pyA2L/pyA2L/pya2l/a2llg.g4 by ANTLR 4.13.2


#include "a2llg.h"


using namespace antlr4;



using namespace antlr4;

namespace {

struct A2llgStaticData final {
  A2llgStaticData(std::vector<std::string> ruleNames,
                          std::vector<std::string> channelNames,
                          std::vector<std::string> modeNames,
                          std::vector<std::string> literalNames,
                          std::vector<std::string> symbolicNames)
      : ruleNames(std::move(ruleNames)), channelNames(std::move(channelNames)),
        modeNames(std::move(modeNames)), literalNames(std::move(literalNames)),
        symbolicNames(std::move(symbolicNames)),
        vocabulary(this->literalNames, this->symbolicNames) {}

  A2llgStaticData(const A2llgStaticData&) = delete;
  A2llgStaticData(A2llgStaticData&&) = delete;
  A2llgStaticData& operator=(const A2llgStaticData&) = delete;
  A2llgStaticData& operator=(A2llgStaticData&&) = delete;

  std::vector<antlr4::dfa::DFA> decisionToDFA;
  antlr4::atn::PredictionContextCache sharedContextCache;
  const std::vector<std::string> ruleNames;
  const std::vector<std::string> channelNames;
  const std::vector<std::string> modeNames;
  const std::vector<std::string> literalNames;
  const std::vector<std::string> symbolicNames;
  const antlr4::dfa::Vocabulary vocabulary;
  antlr4::atn::SerializedATNView serializedATN;
  std::unique_ptr<antlr4::atn::ATN> atn;
};

::antlr4::internal::OnceFlag a2llgLexerOnceFlag;
#if ANTLR4_USE_THREAD_LOCAL_CACHE
static thread_local
#endif
std::unique_ptr<A2llgStaticData> a2llgLexerStaticData = nullptr;

void a2llgLexerInitialize() {
#if ANTLR4_USE_THREAD_LOCAL_CACHE
  if (a2llgLexerStaticData != nullptr) {
    return;
  }
#else
  assert(a2llgLexerStaticData == nullptr);
#endif
  auto staticData = std::make_unique<A2llgStaticData>(
    std::vector<std::string>{
      "IDENT", "EXPONENT", "FLOAT", "INT", "COMMENT", "WS", "STRING", "HEX_DIGIT", 
      "ESC_SEQ", "UNICODE_ESC", "OCTAL_ESC", "BEGIN", "END"
    },
    std::vector<std::string>{
      "DEFAULT_TOKEN_CHANNEL", "HIDDEN"
    },
    std::vector<std::string>{
      "DEFAULT_MODE"
    },
    std::vector<std::string>{
      "", "", "", "", "", "", "", "'/begin'", "'/end'"
    },
    std::vector<std::string>{
      "", "IDENT", "FLOAT", "INT", "COMMENT", "WS", "STRING", "BEGIN", "END"
    }
  );
  static const int32_t serializedATNSegment[] = {
  	4,0,8,188,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
  	6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,1,0,1,0,5,0,30,
  	8,0,10,0,12,0,33,9,0,1,1,1,1,3,1,37,8,1,1,1,4,1,40,8,1,11,1,12,1,41,1,
  	2,3,2,45,8,2,1,2,4,2,48,8,2,11,2,12,2,49,1,2,1,2,5,2,54,8,2,10,2,12,2,
  	57,9,2,1,2,3,2,60,8,2,1,2,1,2,4,2,64,8,2,11,2,12,2,65,1,2,3,2,69,8,2,
  	1,2,4,2,72,8,2,11,2,12,2,73,1,2,1,2,1,2,1,2,1,2,1,2,1,2,3,2,83,8,2,1,
  	3,3,3,86,8,3,1,3,4,3,89,8,3,11,3,12,3,90,1,3,1,3,1,3,4,3,96,8,3,11,3,
  	12,3,97,3,3,100,8,3,1,4,1,4,1,4,1,4,5,4,106,8,4,10,4,12,4,109,9,4,1,4,
  	3,4,112,8,4,1,4,1,4,1,4,1,4,1,4,5,4,119,8,4,10,4,12,4,122,9,4,1,4,1,4,
  	3,4,126,8,4,1,4,1,4,1,5,1,5,1,5,1,5,1,6,1,6,1,6,5,6,137,8,6,10,6,12,6,
  	140,9,6,1,6,1,6,1,7,1,7,1,8,1,8,1,8,1,8,1,8,3,8,151,8,8,1,9,1,9,1,9,1,
  	9,1,9,3,9,158,8,9,3,9,160,8,9,3,9,162,8,9,3,9,164,8,9,1,10,1,10,1,10,
  	1,10,1,10,1,10,1,10,1,10,1,10,3,10,175,8,10,1,11,1,11,1,11,1,11,1,11,
  	1,11,1,11,1,12,1,12,1,12,1,12,1,12,1,120,0,13,1,1,3,0,5,2,7,3,9,4,11,
  	5,13,6,15,0,17,0,19,0,21,0,23,7,25,8,1,0,10,3,0,65,90,95,95,97,122,5,
  	0,46,46,48,57,65,90,95,95,97,122,2,0,69,69,101,101,2,0,43,43,45,45,2,
  	0,88,88,120,120,3,0,48,57,65,70,97,102,2,0,10,10,13,13,3,0,9,10,13,13,
  	32,32,2,0,34,34,92,92,8,0,34,34,39,39,92,92,98,98,102,102,110,110,114,
  	114,116,116,215,0,1,1,0,0,0,0,5,1,0,0,0,0,7,1,0,0,0,0,9,1,0,0,0,0,11,
  	1,0,0,0,0,13,1,0,0,0,0,23,1,0,0,0,0,25,1,0,0,0,1,27,1,0,0,0,3,34,1,0,
  	0,0,5,44,1,0,0,0,7,99,1,0,0,0,9,125,1,0,0,0,11,129,1,0,0,0,13,133,1,0,
  	0,0,15,143,1,0,0,0,17,145,1,0,0,0,19,152,1,0,0,0,21,174,1,0,0,0,23,176,
  	1,0,0,0,25,183,1,0,0,0,27,31,7,0,0,0,28,30,7,1,0,0,29,28,1,0,0,0,30,33,
  	1,0,0,0,31,29,1,0,0,0,31,32,1,0,0,0,32,2,1,0,0,0,33,31,1,0,0,0,34,36,
  	7,2,0,0,35,37,7,3,0,0,36,35,1,0,0,0,36,37,1,0,0,0,37,39,1,0,0,0,38,40,
  	2,48,57,0,39,38,1,0,0,0,40,41,1,0,0,0,41,39,1,0,0,0,41,42,1,0,0,0,42,
  	4,1,0,0,0,43,45,7,3,0,0,44,43,1,0,0,0,44,45,1,0,0,0,45,82,1,0,0,0,46,
  	48,2,48,57,0,47,46,1,0,0,0,48,49,1,0,0,0,49,47,1,0,0,0,49,50,1,0,0,0,
  	50,51,1,0,0,0,51,55,5,46,0,0,52,54,2,48,57,0,53,52,1,0,0,0,54,57,1,0,
  	0,0,55,53,1,0,0,0,55,56,1,0,0,0,56,59,1,0,0,0,57,55,1,0,0,0,58,60,3,3,
  	1,0,59,58,1,0,0,0,59,60,1,0,0,0,60,83,1,0,0,0,61,63,5,46,0,0,62,64,2,
  	48,57,0,63,62,1,0,0,0,64,65,1,0,0,0,65,63,1,0,0,0,65,66,1,0,0,0,66,68,
  	1,0,0,0,67,69,3,3,1,0,68,67,1,0,0,0,68,69,1,0,0,0,69,83,1,0,0,0,70,72,
  	2,48,57,0,71,70,1,0,0,0,72,73,1,0,0,0,73,71,1,0,0,0,73,74,1,0,0,0,74,
  	75,1,0,0,0,75,83,3,3,1,0,76,77,5,78,0,0,77,78,5,97,0,0,78,83,5,78,0,0,
  	79,80,5,73,0,0,80,81,5,78,0,0,81,83,5,70,0,0,82,47,1,0,0,0,82,61,1,0,
  	0,0,82,71,1,0,0,0,82,76,1,0,0,0,82,79,1,0,0,0,83,6,1,0,0,0,84,86,7,3,
  	0,0,85,84,1,0,0,0,85,86,1,0,0,0,86,88,1,0,0,0,87,89,2,48,57,0,88,87,1,
  	0,0,0,89,90,1,0,0,0,90,88,1,0,0,0,90,91,1,0,0,0,91,100,1,0,0,0,92,93,
  	5,48,0,0,93,95,7,4,0,0,94,96,7,5,0,0,95,94,1,0,0,0,96,97,1,0,0,0,97,95,
  	1,0,0,0,97,98,1,0,0,0,98,100,1,0,0,0,99,85,1,0,0,0,99,92,1,0,0,0,100,
  	8,1,0,0,0,101,102,5,47,0,0,102,103,5,47,0,0,103,107,1,0,0,0,104,106,8,
  	6,0,0,105,104,1,0,0,0,106,109,1,0,0,0,107,105,1,0,0,0,107,108,1,0,0,0,
  	108,111,1,0,0,0,109,107,1,0,0,0,110,112,5,13,0,0,111,110,1,0,0,0,111,
  	112,1,0,0,0,112,113,1,0,0,0,113,126,5,10,0,0,114,115,5,47,0,0,115,116,
  	5,42,0,0,116,120,1,0,0,0,117,119,9,0,0,0,118,117,1,0,0,0,119,122,1,0,
  	0,0,120,121,1,0,0,0,120,118,1,0,0,0,121,123,1,0,0,0,122,120,1,0,0,0,123,
  	124,5,42,0,0,124,126,5,47,0,0,125,101,1,0,0,0,125,114,1,0,0,0,126,127,
  	1,0,0,0,127,128,6,4,0,0,128,10,1,0,0,0,129,130,7,7,0,0,130,131,1,0,0,
  	0,131,132,6,5,1,0,132,12,1,0,0,0,133,138,5,34,0,0,134,137,3,17,8,0,135,
  	137,8,8,0,0,136,134,1,0,0,0,136,135,1,0,0,0,137,140,1,0,0,0,138,136,1,
  	0,0,0,138,139,1,0,0,0,139,141,1,0,0,0,140,138,1,0,0,0,141,142,5,34,0,
  	0,142,14,1,0,0,0,143,144,7,5,0,0,144,16,1,0,0,0,145,150,5,92,0,0,146,
  	151,7,9,0,0,147,151,3,19,9,0,148,151,9,0,0,0,149,151,5,0,0,1,150,146,
  	1,0,0,0,150,147,1,0,0,0,150,148,1,0,0,0,150,149,1,0,0,0,151,18,1,0,0,
  	0,152,163,5,117,0,0,153,161,3,15,7,0,154,159,3,15,7,0,155,157,3,15,7,
  	0,156,158,3,15,7,0,157,156,1,0,0,0,157,158,1,0,0,0,158,160,1,0,0,0,159,
  	155,1,0,0,0,159,160,1,0,0,0,160,162,1,0,0,0,161,154,1,0,0,0,161,162,1,
  	0,0,0,162,164,1,0,0,0,163,153,1,0,0,0,163,164,1,0,0,0,164,20,1,0,0,0,
  	165,166,5,92,0,0,166,167,2,48,51,0,167,168,2,48,55,0,168,175,2,48,55,
  	0,169,170,5,92,0,0,170,171,2,48,55,0,171,175,2,48,55,0,172,173,5,92,0,
  	0,173,175,2,48,55,0,174,165,1,0,0,0,174,169,1,0,0,0,174,172,1,0,0,0,175,
  	22,1,0,0,0,176,177,5,47,0,0,177,178,5,98,0,0,178,179,5,101,0,0,179,180,
  	5,103,0,0,180,181,5,105,0,0,181,182,5,110,0,0,182,24,1,0,0,0,183,184,
  	5,47,0,0,184,185,5,101,0,0,185,186,5,110,0,0,186,187,5,100,0,0,187,26,
  	1,0,0,0,28,0,31,36,41,44,49,55,59,65,68,73,82,85,90,97,99,107,111,120,
  	125,136,138,150,157,159,161,163,174,2,0,1,0,6,0,0
  };
  staticData->serializedATN = antlr4::atn::SerializedATNView(serializedATNSegment, sizeof(serializedATNSegment) / sizeof(serializedATNSegment[0]));

  antlr4::atn::ATNDeserializer deserializer;
  staticData->atn = deserializer.deserialize(staticData->serializedATN);

  const size_t count = staticData->atn->getNumberOfDecisions();
  staticData->decisionToDFA.reserve(count);
  for (size_t i = 0; i < count; i++) { 
    staticData->decisionToDFA.emplace_back(staticData->atn->getDecisionState(i), i);
  }
  a2llgLexerStaticData = std::move(staticData);
}

}

a2llg::a2llg(CharStream *input) : Lexer(input) {
  a2llg::initialize();
  _interpreter = new atn::LexerATNSimulator(this, *a2llgLexerStaticData->atn, a2llgLexerStaticData->decisionToDFA, a2llgLexerStaticData->sharedContextCache);
}

a2llg::~a2llg() {
  delete _interpreter;
}

std::string a2llg::getGrammarFileName() const {
  return "a2llg.g4";
}

const std::vector<std::string>& a2llg::getRuleNames() const {
  return a2llgLexerStaticData->ruleNames;
}

const std::vector<std::string>& a2llg::getChannelNames() const {
  return a2llgLexerStaticData->channelNames;
}

const std::vector<std::string>& a2llg::getModeNames() const {
  return a2llgLexerStaticData->modeNames;
}

const dfa::Vocabulary& a2llg::getVocabulary() const {
  return a2llgLexerStaticData->vocabulary;
}

antlr4::atn::SerializedATNView a2llg::getSerializedATN() const {
  return a2llgLexerStaticData->serializedATN;
}

const atn::ATN& a2llg::getATN() const {
  return *a2llgLexerStaticData->atn;
}




void a2llg::initialize() {
#if ANTLR4_USE_THREAD_LOCAL_CACHE
  a2llgLexerInitialize();
#else
  ::antlr4::internal::call_once(a2llgLexerOnceFlag, a2llgLexerInitialize);
#endif
}
