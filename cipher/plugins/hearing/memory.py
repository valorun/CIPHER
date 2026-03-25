import os
import memvid_sdk
from memvid_sdk.embeddings import OllamaEmbeddings

class MemoryManager:
    def __init__(self, memory_path: str = None):
        if memory_path is None:
            memory_path = os.path.join(os.path.dirname(__file__), 'robot_memory.mv2')
        self.memory_path = memory_path
        self.embedder = OllamaEmbeddings(model="all-minilm:22m", dimension=384)

    def add_memory(self, topic: str, content: str):
        """Add a new memory to the robot's knowledge base."""
        with memvid_sdk.use('basic', self.memory_path, enable_vec=True, mode='auto') as mem:
            mem.put_many(
                [
                    {
                        "title": topic,
                        "label": "knowledge",
                        "labels": ["knowledge"],
                        "text": content,
                        "metadata": {}
                    }
                ],
                embedder=self.embedder
            )

    def get_relevant_context(self, query: str, k: int = 3) -> str:
        """Retrieve relevant context for a given query."""
        try:
            with memvid_sdk.use('basic', self.memory_path, enable_vec=True, mode='auto') as mem:
                results = mem.find(query, k=k, embedder=self.embedder, mode='sem')
                
                context_parts = []
                print(results)
                for hit in results.get('hits', []):
                    if 'knowledge' in hit.get('labels', []):
                        clean_text = hit.get('text', '').split('title:')[0].strip()
                        context_parts.append(f"- {hit.get('title')}: {clean_text}")
                        
                if not context_parts:
                    return ""
                    
                return "Souvenirs :\n" + "\n".join(context_parts)
        except Exception as e:
            return ""

    def get_all_memories(self):
        """Retrieve all memories stored in the robot's knowledge base."""
        try:
            with memvid_sdk.use('basic', self.memory_path, enable_vec=True, mode='auto') as mem:
                results = mem.find("knowledge", k=100)
                memories = []
                for hit in results.get('hits', []):
                    if 'knowledge' in hit.get('labels', []):
                        clean_text = hit.get('text', '').split('title:')[0].strip()
                        memories.append({
                            'id': hit.get('frame_id'),
                            'topic': hit.get('title'),
                            'content': clean_text,
                            'timestamp': hit.get('created_at')
                        })
                return memories
        except Exception as e:
            return []
            
    def delete_memory(self, memory_id: int):
        """Delete a memory from the robot's knowledge base."""
        try:
            with memvid_sdk.use('basic', self.memory_path, enable_vec=True, mode='auto') as mem:
                mem.remove(memory_id)
        except Exception as e:
            pass

memory_manager = MemoryManager()
