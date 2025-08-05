#!/usr/bin/env python3
"""
Script to check correlation between AI-generated areas and actual PDF content
"""

def analyze_correlation():
    # Read the extracted PDF content
    with open('simple_extraction_output.txt', 'r', encoding='utf-8') as f:
        pdf_content = f.read().lower()

    ai_areas = [
        'Computer Architecture vs. Organization',
        'Generations of Computers',
        'Computer Types (Digital, Analog, Hybrid, Micro, Mini, Mainframe, Super)',
        'Functional Units of a Computer',
        'Basic Operational Concepts (Instruction Cycle, Interrupts)',
        'Memory Hierarchy (Cache, Primary, Secondary)',
        'Data Representation (Binary, Octal, Hexadecimal, BCD, Complements)',
        'Addressing Modes', 
        'Instruction Formats (Zero, One, Two, Three Address)',
        'RISC vs. CISC Architectures',
        'RAID Levels',
        'Multiprocessor Architectures & Cache Coherence'
    ]

    print('📊 CORRELATION ANALYSIS')
    print('=' * 60)
    print('✅ = Found in PDF    ❌ = NOT Found in PDF')
    print('=' * 60)

    found_count = 0
    details = []
    
    for i, area in enumerate(ai_areas, 1):
        found = False
        evidence = []
        
        # Check for specific topics in the PDF content
        if 'computer architecture' in area.lower() and 'organization' in area.lower():
            if 'computer architecture' in pdf_content and 'computer organization' in pdf_content:
                found = True
                evidence.append("Found: 'Computer Architecture' and 'Computer Organization' definitions")
                
        elif 'generations' in area.lower():
            if 'generation' in pdf_content and ('first generation' in pdf_content or 'second generation' in pdf_content):
                found = True
                evidence.append("Found: Multiple computer generations discussed")
                
        elif 'computer types' in area.lower():
            types_found = [x for x in ['micro', 'mini', 'mainframe', 'supercomputer', 'desktop', 'laptop', 'workstation'] if x in pdf_content]
            if types_found:
                found = True
                evidence.append(f"Found computer types: {', '.join(types_found)}")
                
        elif 'functional units' in area.lower():
            if 'functional unit' in pdf_content or ('input unit' in pdf_content and 'output unit' in pdf_content):
                found = True
                evidence.append("Found: Functional units discussion")
                
        elif 'instruction cycle' in area.lower() or 'interrupt' in area.lower():
            if 'instruction' in pdf_content and ('interrupt' in pdf_content or 'cycle' in pdf_content):
                found = True
                evidence.append("Found: Instructions and interrupts discussed")
                
        elif 'memory hierarchy' in area.lower():
            if 'cache memory' in pdf_content and ('primary memory' in pdf_content or 'secondary memory' in pdf_content):
                found = True
                evidence.append("Found: Cache, primary, and secondary memory")
                
        elif 'data representation' in area.lower():
            formats_found = [x for x in ['binary', 'octal', 'hexadecimal', 'bcd', 'complement'] if x in pdf_content]
            if formats_found:
                found = True
                evidence.append(f"Found data formats: {', '.join(formats_found)}")
                
        elif 'addressing modes' in area.lower():
            if 'addressing' in pdf_content:
                found = True
                evidence.append("Found: Addressing concepts")
                
        elif 'instruction formats' in area.lower():
            if 'instruction format' in pdf_content or 'opcode' in pdf_content:
                found = True
                evidence.append("Found: Instruction formats and opcodes")
                
        elif 'risc' in area.lower() and 'cisc' in area.lower():
            if 'risc' in pdf_content and 'cisc' in pdf_content:
                found = True
                evidence.append("Found: RISC vs CISC comparison")
                
        elif 'raid' in area.lower():
            if 'raid' in pdf_content:
                found = True
                evidence.append("Found: RAID levels discussion")
                
        elif 'multiprocessor' in area.lower():
            if 'multiprocessor' in pdf_content and 'cache coherence' in pdf_content:
                found = True
                evidence.append("Found: Multiprocessors and cache coherence")
        
        if found:
            found_count += 1
            print(f'✅ {i:2d}. {area}')
            details.append((area, True, evidence))
        else:
            print(f'❌ {i:2d}. {area}')
            details.append((area, False, []))

    print()
    print(f'📈 CORRELATION SCORE: {found_count}/{len(ai_areas)} ({found_count/len(ai_areas)*100:.1f}%)')
    print()
    
    if found_count >= 8:
        print('🎯 EXCELLENT correlation! The AI did very well.')
    elif found_count >= 6:
        print('👍 GOOD correlation! Most areas match the content.')
    elif found_count >= 4:
        print('⚠️  MODERATE correlation. Some areas do not match.')
    else:
        print('❌ POOR correlation. AI may have hallucinated content.')
    
    print()
    print('🔍 DETAILED EVIDENCE:')
    print('=' * 60)
    for area, found, evidence in details:
        if found and evidence:
            print(f"✅ {area}:")
            for e in evidence:
                print(f"   • {e}")
            print()

if __name__ == "__main__":
    analyze_correlation()
