
// Generated from D:/a/pyA2L/pyA2L/pya2l/a2llg.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"




class  a2llg : public antlr4::Lexer {
public:
  enum {
    IDENT = 1, FLOAT = 2, INT = 3, COMMENT = 4, WS = 5, STRING = 6, BEGIN = 7, 
    END = 8
  };

  explicit a2llg(antlr4::CharStream *input);

  ~a2llg() override;


  std::string getGrammarFileName() const override;

  const std::vector<std::string>& getRuleNames() const override;

  const std::vector<std::string>& getChannelNames() const override;

  const std::vector<std::string>& getModeNames() const override;

  const antlr4::dfa::Vocabulary& getVocabulary() const override;

  antlr4::atn::SerializedATNView getSerializedATN() const override;

  const antlr4::atn::ATN& getATN() const override;

  // By default the static state used to implement the lexer is lazily initialized during the first
  // call to the constructor. You can call this function if you wish to initialize the static state
  // ahead of time.
  static void initialize();

private:

  // Individual action functions triggered by action() above.

  // Individual semantic predicate functions triggered by sempred() above.

};

