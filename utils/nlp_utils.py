def generate_nlp_review(class1, class2, counts1, counts2):
    review = ""
    if class1 == class2:
        review += f"The landscape remained predominantly {class1.lower()}, indicating stability in land use."
    else:
        review += f"Significant change detected: {class1} → {class2}. "
        if class1 == "Forest" and class2 == "Agriculture":
            review += "Possible deforestation event for agricultural expansion. Monitor biodiversity and soil health."
        elif class1 == "Agriculture" and class2 == "Urban":
            review += "Urbanization of agricultural land detected. Urban planning and food security should be considered."
        elif class1 == "Water" and class2 == "BarrenLand":
            review += "Water body drying observed, possibly due to drought or diversion. Assess water management."
        elif class1 == "BarrenLand" and class2 == "Water":
            review += "New water body formation or flooding detected. Check for seasonal or climatic effects."
        else:
            review += "Transition observed; field verification recommended for accurate interpretation."
    # Add actionable recommendations
    review += "\n\nRecommendations:\n"
    if class1 != class2:
        review += "- Conduct ground validation\n"
        if "Urban" in [class1, class2]:
            review += "- Assess sustainable development strategies\n"
        if "Water" in [class1, class2]:
            review += "- Implement water conservation measures\n"
        if "Forest" in [class1, class2]:
            review += "- Monitor biodiversity and prevent illegal clearing\n"
    else:
        review += "- Continue monitoring for subtle changes\n"
    return review
