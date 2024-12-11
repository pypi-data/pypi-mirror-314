import torch
from ts.torch_handler.base_handler import BaseHandler
from radgraph import RadGraph  # Import your model class


class RadGraphHandler(BaseHandler):
    def initialize(self, context):
        # Load model weights
        properties = context.system_properties
        model_dir = properties.get("model_dir")
        device = torch.device("cpu")

        # Create model instance
        self.model = RadGraph(model_type="radgraph-xl", cuda=None)
        state_dict = torch.load(f"{model_dir}/model_weights.pth", map_location=device)
        self.model.model.load_state_dict(state_dict)
        self.model.model.to(device)
        self.model.model.eval()

        self.initialized = True

    def handle(self, data, context):
        # data is a list of requests
        # Each request is expected to contain the text to process
        inputs = []
        for request in data:
            if isinstance(request, dict) and "body" in request:
                text = request["body"]
                if isinstance(text, bytes):
                    text = text.decode('utf-8')
                inputs.append(text)
            else:
                inputs.append(request)

        # Run inference
        with torch.no_grad():
            output = self.model(inputs)

        return [output]
