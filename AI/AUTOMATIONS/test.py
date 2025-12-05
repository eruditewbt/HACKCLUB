    def analyze_and_recommend(self):
        """Analyzes user input against the knowledge base to make recommendations."""
        print("\n--- Analyzing Project Characteristics and Making Recommendations ---")

        # Prioritize matching Life Cycle and Methodologies first as they often drive others
        matched_life_cycles = self._find_matches("Life Cycle", top_n=3)
        if matched_life_cycles:
            self.recommendations["Life Cycle"] = matched_life_cycles
            print(f"Recommended Life Cycles: {', '.join(matched_life_cycles)}")
            self.project_characteristics["Life Cycle"] = matched_life_cycles

        matched_methodologies = self._find_matches("Methodology", top_n=3)
        if matched_methodologies:
            self.recommendations["Methodology"] = matched_methodologies
            print(f"Recommended Methodologies: {', '.join(matched_methodologies)}")

        # General recommendations for other categories
        for category in ["Language", "Model (Architectural)", "Timeframe Management"]:
            matched_items = self._find_matches(category, top_n=3)
            if matched_items:
                self.recommendations[category] = matched_items
                print(f"Recommended {category}: {', '.join(matched_items)}")

        #self._add_general_considerations()

    def _find_matches(self, category_key, top_n=3):
        """
        Finds the top N items in the knowledge base that best match the project characteristics
        for a given category (e.g., "Life Cycle").
        """
        kbCategory=self.knowledge_base.get(category_key)
        scored_matches = []
        for item, criteria in kbCategory.items():
            # Instead of restricting by category, score all KB items
            score = 0
            total = 0
            is_possible = True
            for char_key, char_values in criteria.items():
                total += 1
                if char_key in self.project_characteristics:
                    user_value = self.project_characteristics[char_key]
                    if user_value in char_values or (char_key == "Life Cycle" and any(lc in char_values for lc in self.recommendations.get("Life Cycle", []))):
                        score += 1
                    else:
                        is_possible = False
                        break
                elif char_key.endswith("(Implicit)"):
                    inferred_key = char_key.replace(" (Implicit)", "")
                    if inferred_key in self.project_characteristics and self.project_characteristics[inferred_key] in char_values:
                        score += 1
                    else:
                        is_possible = False
                        break
                elif char_key in ["Scalability Needs", "Real-time Processing", "DevOps Implemented"]:
                    if char_key in self.project_characteristics and self.project_characteristics[char_key] in char_values:
                        score += 1
                    else:
                        is_possible = False
                        break
                else:
                    is_possible = False
                    break
            if is_possible and score > 0:
                scored_matches.append((score / total if total else 0, score, item))
        # Sort by highest score (fraction matched, then absolute number matched), then alphabetically
        scored_matches.sort(reverse=True)
        # Return only the top N matches
        return [item for _, _, item in scored_matches[:top_n]]