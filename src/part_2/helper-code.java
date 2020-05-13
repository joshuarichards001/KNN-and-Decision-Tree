/* Build the Decision Tree */
    Node buildTree(ArrayList<String> attributeLabels, ArrayList<Boolean[]> instances) {

        Node node;

        Double[] best_attribute_information = DetermineNextSplit(attributeLabels, instances);

        int best_attribute_index = best_attribute_information[0].intValue();
        String best_attribute = attributeLabels.get(best_attribute_index);

        System.out.println("Best attribute : " + best_attribute);
        System.out.println("Index : " + best_attribute_index);
        System.out.println("Information Gain : " + best_attribute_information[1]);

        Calculate_Information_Gain best_attribute_information_gain = new Calculate_Information_Gain();
        best_attribute_information_gain.splitByAttribute(instances, best_attribute_index);

        ArrayList<Boolean[]> best_attribute_true_split =  best_attribute_information_gain.getTrue_split();
        ArrayList<Boolean[]> best_attribute_false_split = best_attribute_information_gain.getFalse_split();

        if(best_attribute_information[1] == 1){

            String left_prediction, right_prediction;

            if (!best_attribute_true_split.isEmpty()) {
                if (best_attribute_true_split.get(0)[0] == true) {
                    left_prediction = "live";
                    right_prediction = "die";
                } else {
                    left_prediction = "die";
                    right_prediction = "live";
                }
            } else {
                if (best_attribute_false_split.get(0)[0] == true) {
                    right_prediction = "live";
                    left_prediction = "die";
                } else {
                    right_prediction = "die";
                    left_prediction = "live";
                }
            }

            node = new Node(best_attribute, left_prediction, right_prediction);
        }

        else if(best_attribute_information[1] == 0){

            int true_instances = 0;
            String split;
            ArrayList<Boolean[]> instances_of_class;

            if(!best_attribute_true_split.isEmpty()){
                split = "true";
                instances_of_class = best_attribute_true_split;
            }
            else{
                split = "false";
                instances_of_class = best_attribute_false_split;
            }

            for(Boolean[] instance : instances_of_class){
                if(instance[0] == true){
                    true_instances++;
                }
            }
            int false_instances = instances_of_class.size() - true_instances;

            String left_prediction, right_prediction;

            if((split.equals("true") && true_instances >= false_instances) ||
                    split.equals("false") && false_instances > true_instances){
                left_prediction = "live";
                right_prediction = "die";
            }
            else{
                left_prediction = "die";
                right_prediction = "live";
            }

            node = new Node(best_attribute, left_prediction, right_prediction);
        }
        else{
            attributeLabels.remove(best_attribute);
            for(Boolean[] instance : best_attribute_true_split){
                deleteIndex(instance, best_attribute_index);
            }
            for(Boolean[] instance : best_attribute_false_split){
                deleteIndex(instance, best_attribute_index);
            }

            node = new Node(best_attribute);

            node.left = buildTree(attributeLabels, best_attribute_true_split);
            node.right = buildTree(attributeLabels, best_attribute_false_split);

            if(root == null){
                root = node;
            }
        }
        return node;
    }