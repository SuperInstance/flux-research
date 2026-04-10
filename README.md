# flux-research

Deep research on compilers, interpreters, and agent-first runtime design for the FLUX ecosystem.

## Documents

### [compiler-interpreter-deep-dive.md](compiler-interpreter-deep-dive.md)
~22K words. Comprehensive taxonomy of 6 runtime architectures:
- Stack-based (JVM, WASM, Forth)
- Register-based (Lua, FLUX)
- Tree-walking (Ruby <1.9)
- Compiler-to-native (C, Rust)
- JIT hybrids (V8, LuaJIT)
- Transpilers

Plus: comparative analysis of 8 language VMs, what each taught us, ESP32/embedded strategy.

### [flux-strategic-vision.md](flux-strategic-vision.md)
~10K words. Agent-first computing philosophy:
- Why markdown→bytecode is the kill app
- Agent execution model vs traditional
- Git-agent connection
- FLUX on simple devices (ESP32)
- Universal bytecode translator

### [flux-isa-v2-proposal.md](flux-isa-v2-proposal.md)
~7.5K words. Proposed unified ISA:
- Fixed 4-byte instructions
- Unified 3-operand arithmetic
- Flag-based conditional jumps
- Memory operations, function calls, SYSCALL
- A2A as opcodes, speculative execution

## Key Insight
> We are not building a compiler or interpreter in the traditional sense. We are building something that is both and neither — an openinterpreter-like free flow of ideas to actions that can move between bytecode and markdown.
